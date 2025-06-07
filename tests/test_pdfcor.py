import unittest
import os
import shutil
import fitz  # PyMuPDF
from PIL import Image
import argparse # For CLI testing, though main is usually called directly
import io
from contextlib import redirect_stdout
from unittest.mock import patch

# Adjust import paths
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from pdfcor.core import process_pdf, merge_pdfs, extract_pages
from pdfcor.utils import slugify, resize_for_a4 # resize_for_a4 for checking resized image dimensions
from pdfcor.cli import main as cli_main

class TestPdfCor(unittest.TestCase):

    def setUp(self):
        self.test_input_dir = "test_input"
        self.test_output_dir = "test_output"
        os.makedirs(self.test_input_dir, exist_ok=True)
        os.makedirs(self.test_output_dir, exist_ok=True)

        os.makedirs(self.test_input_dir, exist_ok=True)
        os.makedirs(self.test_output_dir, exist_ok=True)

        # sys.argv patching will be done per-test method for CLI tests


    def tearDown(self):
        if os.path.exists(self.test_input_dir):
            shutil.rmtree(self.test_input_dir)
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)

        # No global patcher to stop here now


    def _create_dummy_pdf(self, filepath, text_contents):
        doc = fitz.open()
        if isinstance(text_contents, str):
            text_contents = [text_contents]
        for text_content in text_contents:
            page = doc.new_page()
            page.insert_text((50, 72), str(text_content), fontsize=11)
        doc.save(filepath)
        doc.close()

    def _create_dummy_image(self, filepath, size=(100, 100), color="blue"):
        img = Image.new('RGB', size, color=color)
        img.save(filepath)

    def _create_pdf_with_image(self, pdf_filepath, image_filepath, image_rect=fitz.Rect(50, 100, 150, 200)):
        doc = fitz.open()
        page = doc.new_page()
        try:
            page.insert_image(image_rect, filename=image_filepath)
        except Exception as e:
            # Fallback for older PyMuPDF versions or different API expectations if any
            print(f"Warning: page.insert_image failed with {e}, trying stream.")
            with open(image_filepath, "rb") as img_file:
                img_bytes = img_file.read()
            page.insert_image(image_rect, stream=img_bytes)
        doc.save(pdf_filepath)
        doc.close()

    def test_process_pdf_extraction(self):
        pdf_path = os.path.join(self.test_input_dir, "sample1.pdf")
        md_output_dir = os.path.join(self.test_output_dir, "markdown_out")
        os.makedirs(md_output_dir, exist_ok=True)
        self._create_dummy_pdf(pdf_path, "Hello World Page 1")
        process_pdf(pdf_path, md_output_dir, resize=False)
        expected_md_file = os.path.join(md_output_dir, "sample1.md")
        self.assertTrue(os.path.exists(expected_md_file))
        with open(expected_md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("# sample1", content)
        self.assertIn("Hello World Page 1", content)

    def test_merge_pdfs_basic(self):
        doc1_path = os.path.join(self.test_input_dir, "doc1.pdf")
        doc2_path = os.path.join(self.test_input_dir, "doc2.pdf")
        self._create_dummy_pdf(doc1_path, "Content Doc1")
        self._create_dummy_pdf(doc2_path, "Content Doc2")
        merged_output_file = "merged.pdf"
        merge_pdfs(self.test_input_dir, output_file=merged_output_file, output_dir=self.test_output_dir)
        expected_merged_path = os.path.join(self.test_output_dir, merged_output_file)
        self.assertTrue(os.path.exists(expected_merged_path))
        merged_doc = fitz.open(expected_merged_path)
        self.assertEqual(len(merged_doc), 2)
        self.assertIn("Content Doc1", merged_doc[0].get_text())
        self.assertIn("Content Doc2", merged_doc[1].get_text())
        merged_doc.close()

    def test_extract_pages_basic(self):
        multipage_pdf_path = os.path.join(self.test_input_dir, "multipage.pdf")
        self._create_dummy_pdf(multipage_pdf_path, ["Page 1 Text", "Page 2 Text"])
        extract_pages(multipage_pdf_path)
        pdf_name_slug = slugify("multipage")
        expected_pages_dir = os.path.join(os.path.dirname(multipage_pdf_path), f"pages-{pdf_name_slug}")
        self.assertTrue(os.path.exists(expected_pages_dir))
        page1_file = os.path.join(expected_pages_dir, f"{pdf_name_slug}-01.pdf")
        page2_file = os.path.join(expected_pages_dir, f"{pdf_name_slug}-02.pdf")
        self.assertTrue(os.path.exists(page1_file))
        self.assertTrue(os.path.exists(page2_file))
        doc1 = fitz.open(page1_file)
        self.assertIn("Page 1 Text", doc1[0].get_text())
        doc1.close()
        doc2 = fitz.open(page2_file)
        self.assertIn("Page 2 Text", doc2[0].get_text())
        doc2.close()

    def test_process_pdf_with_image_extraction(self):
        dummy_image_path = os.path.join(self.test_input_dir, "dummy.png")
        self._create_dummy_image(dummy_image_path)
        pdf_path = os.path.join(self.test_input_dir, "doc_with_image.pdf")
        self._create_pdf_with_image(pdf_path, dummy_image_path)

        output_dir = os.path.join(self.test_output_dir, "img_extract_out")
        process_pdf(pdf_path, output_dir, resize=False)

        expected_md_file = os.path.join(output_dir, "doc_with_image.md")
        self.assertTrue(os.path.exists(expected_md_file))

        slug_pdf_name = slugify("doc_with_image")
        expected_img_dir = os.path.join(output_dir, f"img-{slug_pdf_name}")
        self.assertTrue(os.path.exists(expected_img_dir))

        # Expecting one image, check if any .png file exists (extension might vary: jpg, png)
        found_images = [f for f in os.listdir(expected_img_dir) if f.startswith(slug_pdf_name) and (f.endswith(".png") or f.endswith(".jpg"))]
        self.assertTrue(len(found_images) > 0, "No image file found in output.")
        expected_image_file_name_in_md = f"img-{slug_pdf_name}/{found_images[0]}"

        with open(expected_md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn(f"![Image 1]({expected_image_file_name_in_md})", content)


    def test_process_pdf_with_image_resize(self):
        large_image_path = os.path.join(self.test_input_dir, "large_image.png")
        original_size = (1000, 1200) # W, H
        self._create_dummy_image(large_image_path, size=original_size, color="red")

        pdf_path = os.path.join(self.test_input_dir, "doc_with_large_image.pdf")
        self._create_pdf_with_image(pdf_path, large_image_path)

        output_dir = os.path.join(self.test_output_dir, "img_resize_out")
        process_pdf(pdf_path, output_dir, resize=True)

        slug_pdf_name = slugify("doc_with_large_image")
        expected_img_dir = os.path.join(output_dir, f"img-{slug_pdf_name}")
        self.assertTrue(os.path.exists(expected_img_dir))

        found_images = [f for f in os.listdir(expected_img_dir) if f.startswith(slug_pdf_name)]
        self.assertTrue(len(found_images) > 0, "No resized image file found.")
        extracted_image_path = os.path.join(expected_img_dir, found_images[0])

        img = Image.open(extracted_image_path)
        w, h = img.size
        img.close() # Close the image file

        # Calculate expected dimensions based on resize_for_a4 logic
        a4_width_mm, a4_height_mm = 210, 297
        dpi = 300
        max_w_px = int(a4_width_mm / 25.4 * dpi)
        max_h_px = int(a4_height_mm / 25.4 * dpi)

        ratio = min(max_w_px / original_size[0], max_h_px / original_size[1])
        expected_w = int(original_size[0] * ratio)
        expected_h = int(original_size[1] * ratio)

        self.assertEqual(w, expected_w, "Resized image width is not as expected.")
        self.assertEqual(h, expected_h, "Resized image height is not as expected.")
        self.assertTrue(w <= max_w_px, f"Resized width {w} exceeds A4 max width {max_w_px}")
        self.assertTrue(h <= max_h_px, f"Resized height {h} exceeds A4 max height {max_h_px}")


    def test_cli_markdown_default_output_folder(self):
        abs_input_dir = os.path.abspath(self.test_input_dir)
        pdf_path = os.path.join(abs_input_dir, "cli_doc.pdf")
        self._create_dummy_pdf(pdf_path, "CLI Test Content")

        test_argv = ['pdfcor', '--input-folder', abs_input_dir]
        with patch.object(sys, 'argv', test_argv):
            cli_main()

        expected_md_file = os.path.join(abs_input_dir, "pdfcor_output", "cli_doc.md")
        self.assertTrue(os.path.exists(expected_md_file), f"Expected MD file not found at {expected_md_file}")

    def test_cli_fusion_custom_output_file(self):
        abs_input_dir = os.path.abspath(self.test_input_dir)
        abs_output_dir = os.path.abspath(self.test_output_dir)

        doc1 = os.path.join(abs_input_dir, "fuse1.pdf")
        doc2 = os.path.join(abs_input_dir, "fuse2.pdf")
        self._create_dummy_pdf(doc1, "Fuse 1 content")
        self._create_dummy_pdf(doc2, "Fuse 2 content")

        output_pdf_path = os.path.join(abs_output_dir, "fused_cli.pdf")
        # os.makedirs(abs_output_dir, exist_ok=True) # merge_pdfs (via core) should handle this. cli.py does not for fusion.

        test_argv = ['pdfcor', '--fusion', '--input-folder', abs_input_dir, '--output-file', output_pdf_path]
        with patch.object(sys, 'argv', test_argv):
            cli_main()

        self.assertTrue(os.path.exists(output_pdf_path), f"Fused CLI output PDF not found at {output_pdf_path}")
        merged_doc = fitz.open(output_pdf_path)
        self.assertEqual(len(merged_doc), 2)
        merged_doc.close()

    def test_cli_process_folder_recursive(self):
        abs_input_dir = os.path.abspath(self.test_input_dir)
        abs_output_dir = os.path.abspath(self.test_output_dir)

        sub_folder_path = os.path.join(abs_input_dir, "subfolder")
        os.makedirs(sub_folder_path, exist_ok=True)
        pdf_path = os.path.join(sub_folder_path, "rec_doc.pdf")
        self._create_dummy_pdf(pdf_path, "Recursive Test Content")

        output_dir_rec_abs = os.path.join(abs_output_dir, "rec_out")

        test_argv = ['pdfcor', '--input-folder', abs_input_dir, '--output-folder', output_dir_rec_abs, '--recursive']
        with patch.object(sys, 'argv', test_argv):
            cli_main()

        # The output MD file should be in output_dir_rec_abs
        expected_md_file = os.path.join(output_dir_rec_abs, "rec_doc.md")
        self.assertTrue(os.path.exists(expected_md_file), f"Expected MD file not found at {expected_md_file}")


if __name__ == '__main__':
    unittest.main()
