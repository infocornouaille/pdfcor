import shutil

# Adjust import paths
import sys
import unittest
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image

# import argparse # No longer needed for CLI tests
# import io # Potentially no longer needed
# from contextlib import redirect_stdout # No longer needed
# from unittest.mock import patch # No longer needed for sys.argv
from typer.testing import CliRunner  # Added

parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))  # sys.path expects strings

from pdfcor.cli import app as cli_app  # noqa: E402
from pdfcor.core import extract_pages, merge_pdfs, process_pdf  # noqa: E402
from pdfcor.utils import slugify  # noqa: E402


class TestPdfCor(unittest.TestCase):
    def setUp(self):
        self.test_input_path = Path("test_input")
        self.test_output_path = Path("test_output")

        self.test_input_path.mkdir(parents=True, exist_ok=True)
        self.test_output_path.mkdir(parents=True, exist_ok=True)

        self.runner = CliRunner()  # Instantiate CliRunner

    def tearDown(self):
        if self.test_input_path.exists():
            shutil.rmtree(self.test_input_path)
        if self.test_output_path.exists():
            shutil.rmtree(self.test_output_path)

        # No global patcher to stop here now

    def _create_dummy_pdf(
        self, filepath: Path, text_contents: list[str] | str
    ):  # Allow Path object
        doc = fitz.open()
        if isinstance(text_contents, str):
            text_contents = [text_contents]
        for text_content in text_contents:
            page = doc.new_page()
            page.insert_text((50, 72), str(text_content), fontsize=11)
        doc.save(str(filepath))  # fitz might prefer str
        doc.close()

    def _create_dummy_image(
        self, filepath: Path, size=(100, 100), color="blue"
    ):  # Allow Path object
        img = Image.new("RGB", size, color=color)
        img.save(filepath)  # PIL Image.save can handle Path objects

    def _create_pdf_with_image(
        self,
        pdf_filepath: Path,
        image_filepath: Path,
        image_rect=fitz.Rect(50, 100, 150, 200),
    ):  # Allow Path
        doc = fitz.open()
        page = doc.new_page()
        try:
            # fitz page.insert_image typically expects a string path for filename
            page.insert_image(image_rect, filename=str(image_filepath))
        except Exception as e:
            print(
                f"Warning: page.insert_image with filename failed ({e}), trying stream."
            )
            with open(image_filepath, "rb") as img_file:
                img_bytes = img_file.read()
            page.insert_image(image_rect, stream=img_bytes)
        doc.save(str(pdf_filepath))  # fitz might prefer str
        doc.close()

    def test_process_pdf_extraction(self):
        pdf_path: Path = self.test_input_path / "sample1.pdf"
        md_output_dir: Path = self.test_output_path / "markdown_out"
        md_output_dir.mkdir(
            parents=True, exist_ok=True
        )  # process_pdf expects output_dir to exist
        self._create_dummy_pdf(pdf_path, "Hello World Page 1")

        process_pdf(pdf_path, md_output_dir, resize=False)

        expected_md_file: Path = md_output_dir / f"{pdf_path.stem}.md"
        self.assertTrue(expected_md_file.exists())
        with expected_md_file.open("r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn(f"# {pdf_path.stem}", content)
        self.assertIn("Hello World Page 1", content)

    def test_merge_pdfs_basic(self):
        doc1_path: Path = self.test_input_path / "doc1.pdf"
        doc2_path: Path = self.test_input_path / "doc2.pdf"
        self._create_dummy_pdf(doc1_path, "Content Doc1")
        self._create_dummy_pdf(doc2_path, "Content Doc2")

        merged_output_filename: str = "merged.pdf"
        # Call with Path objects for directories
        merge_pdfs(
            self.test_input_path,
            output_file=merged_output_filename,
            output_dir=self.test_output_path,
        )

        expected_merged_path: Path = self.test_output_path / merged_output_filename
        self.assertTrue(expected_merged_path.exists())

        merged_doc = fitz.open(str(expected_merged_path))  # fitz might prefer str
        self.assertEqual(len(merged_doc), 2)
        self.assertIn("Content Doc1", merged_doc[0].get_text())
        self.assertIn("Content Doc2", merged_doc[1].get_text())
        merged_doc.close()

    def test_extract_pages_basic(self):
        multipage_pdf_path: Path = self.test_input_path / "multipage.pdf"
        self._create_dummy_pdf(multipage_pdf_path, ["Page 1 Text", "Page 2 Text"])

        extract_pages(multipage_pdf_path)  # Call with Path object

        pdf_name_slug: str = slugify(multipage_pdf_path.stem)
        # extract_pages creates output in pdf_path.parent / f"pages-{slug}"
        expected_pages_dir: Path = multipage_pdf_path.parent / f"pages-{pdf_name_slug}"

        self.assertTrue(expected_pages_dir.exists())

        page1_file: Path = expected_pages_dir / f"{pdf_name_slug}-01.pdf"
        page2_file: Path = expected_pages_dir / f"{pdf_name_slug}-02.pdf"

        self.assertTrue(page1_file.exists())
        self.assertTrue(page2_file.exists())

        doc1 = fitz.open(str(page1_file))  # fitz might prefer str
        self.assertIn("Page 1 Text", doc1[0].get_text())
        doc1.close()

        doc2 = fitz.open(str(page2_file))  # fitz might prefer str
        self.assertIn("Page 2 Text", doc2[0].get_text())
        doc2.close()

    def test_process_pdf_with_image_extraction(self):
        dummy_image_path: Path = self.test_input_path / "dummy.png"
        self._create_dummy_image(dummy_image_path)
        pdf_path: Path = self.test_input_path / "doc_with_image.pdf"
        self._create_pdf_with_image(pdf_path, dummy_image_path)

        output_dir: Path = self.test_output_path / "img_extract_out"
        output_dir.mkdir(parents=True, exist_ok=True)
        process_pdf(pdf_path, output_dir, resize=False)

        expected_md_file: Path = output_dir / f"{pdf_path.stem}.md"
        self.assertTrue(expected_md_file.exists())

        slug_pdf_name: str = slugify(pdf_path.stem)
        expected_img_dir: Path = output_dir / f"img-{slug_pdf_name}"
        self.assertTrue(expected_img_dir.exists())

        found_images = [
            f.name
            for f in expected_img_dir.iterdir()
            if f.name.startswith(slug_pdf_name)
            and (f.name.endswith(".png") or f.name.endswith(".jpg"))
        ]
        self.assertTrue(len(found_images) > 0, "No image file found in output.")
        expected_image_file_name_in_md = f"img-{slug_pdf_name}/{found_images[0]}"

        with expected_md_file.open("r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn(f"![Image 1]({expected_image_file_name_in_md})", content)

    def test_process_pdf_with_image_resize(self):
        large_image_path: Path = self.test_input_path / "large_image.png"
        original_size = (1000, 1200)  # W, H
        self._create_dummy_image(large_image_path, size=original_size, color="red")

        pdf_path: Path = self.test_input_path / "doc_with_large_image.pdf"
        self._create_pdf_with_image(pdf_path, large_image_path)

        output_dir: Path = self.test_output_path / "img_resize_out"
        output_dir.mkdir(parents=True, exist_ok=True)
        process_pdf(pdf_path, output_dir, resize=True)

        slug_pdf_name: str = slugify(pdf_path.stem)
        expected_img_dir: Path = output_dir / f"img-{slug_pdf_name}"
        self.assertTrue(expected_img_dir.exists())

        found_images_resized = [
            f for f in expected_img_dir.iterdir() if f.name.startswith(slug_pdf_name)
        ]
        self.assertTrue(len(found_images_resized) > 0, "No resized image file found.")
        extracted_image_path: Path = found_images_resized[0]

        img = Image.open(extracted_image_path)  # PIL Image.open can handle Path
        w, h = img.size
        img.close()  # Close the image file

        # Calculate expected dimensions based on resize_for_a4 logic from utils
        a4_width_mm, a4_height_mm = 210, 297
        dpi = 300
        max_w_px = int(a4_width_mm / 25.4 * dpi)
        max_h_px = int(a4_height_mm / 25.4 * dpi)

        ratio = min(max_w_px / original_size[0], max_h_px / original_size[1])  # type: ignore
        expected_w = int(original_size[0] * ratio)  # type: ignore
        expected_h = int(original_size[1] * ratio)  # type: ignore

        self.assertEqual(w, expected_w, "Resized image width is not as expected.")
        self.assertEqual(h, expected_h, "Resized image height is not as expected.")
        self.assertTrue(
            w <= max_w_px, f"Resized width {w} exceeds A4 max width {max_w_px}"
        )
        self.assertTrue(
            h <= max_h_px, f"Resized height {h} exceeds A4 max height {max_h_px}"
        )

    def test_cli_process_default_output(self):  # Renamed
        abs_input_dir: Path = self.test_input_path.resolve()
        pdf_on_input_path: Path = abs_input_dir / "cli_doc.pdf"
        self._create_dummy_pdf(
            pdf_on_input_path, "CLI Test Content for process default"
        )

        result = self.runner.invoke(
            cli_app, ["process", "--input-folder", str(abs_input_dir)]
        )

        self.assertEqual(result.exit_code, 0, result.stdout)
        expected_md_file: Path = abs_input_dir / "pdfcor_output" / "cli_doc.md"
        self.assertTrue(
            expected_md_file.exists(),
            f"Expected MD file not found at {expected_md_file}\nOutput:\n{result.stdout}",
        )

    def test_cli_merge_custom_output(self):  # Renamed
        abs_input_dir: Path = self.test_input_path.resolve()
        abs_output_dir: Path = self.test_output_path.resolve()

        doc1_path: Path = abs_input_dir / "fuse1.pdf"
        doc2_path: Path = abs_input_dir / "fuse2.pdf"
        self._create_dummy_pdf(doc1_path, "Fuse 1 content")
        self._create_dummy_pdf(doc2_path, "Fuse 2 content")

        output_pdf_file_path: Path = abs_output_dir / "fused_cli.pdf"

        result = self.runner.invoke(
            cli_app,
            [
                "merge",
                "--input-folder",
                str(abs_input_dir),
                "--output-file",
                str(output_pdf_file_path),
            ],
        )

        self.assertEqual(result.exit_code, 0, result.stdout)
        self.assertTrue(
            output_pdf_file_path.exists(),
            f"Fused CLI output PDF not found at {output_pdf_file_path}\nOutput:\n{result.stdout}",
        )
        merged_doc = fitz.open(str(output_pdf_file_path))
        self.assertEqual(len(merged_doc), 2)
        merged_doc.close()

    def test_cli_process_recursive(self):  # Renamed
        abs_input_dir: Path = self.test_input_path.resolve()
        abs_output_dir: Path = self.test_output_path.resolve()

        sub_folder: Path = abs_input_dir / "subfolder"
        sub_folder.mkdir(parents=True, exist_ok=True)
        pdf_in_subfolder: Path = sub_folder / "rec_doc.pdf"
        self._create_dummy_pdf(pdf_in_subfolder, "Recursive Test Content")

        output_dir_rec: Path = abs_output_dir / "rec_out"

        result = self.runner.invoke(
            cli_app,
            [
                "process",
                "--input-folder",
                str(abs_input_dir),
                "--output-folder",
                str(output_dir_rec),
                "--recursive",
            ],
        )

        self.assertEqual(result.exit_code, 0, result.stdout)
        expected_md_file: Path = output_dir_rec / "rec_doc.md"
        self.assertTrue(
            expected_md_file.exists(),
            f"Expected MD file not found at {expected_md_file}\nOutput:\n{result.stdout}",
        )

    def test_cli_extract(self):  # New test
        multipage_pdf_path: Path = self.test_input_path / "multipage_cli.pdf"
        self._create_dummy_pdf(
            multipage_pdf_path, ["CLI Page 1 Text", "CLI Page 2 Text"]
        )

        # Resolve path for the argument as Typer would if exists=True, resolve_path=True were on Argument
        # However, CliRunner takes strings, so we resolve it manually for the test's expectation.
        resolved_multipage_pdf_path_str = str(multipage_pdf_path.resolve())

        result = self.runner.invoke(
            cli_app, ["extract", resolved_multipage_pdf_path_str]
        )

        self.assertEqual(result.exit_code, 0, result.stdout)

        pdf_name_slug: str = slugify(multipage_pdf_path.stem)
        expected_pages_dir: Path = multipage_pdf_path.parent / f"pages-{pdf_name_slug}"

        self.assertTrue(
            expected_pages_dir.exists(),
            f"Extracted pages directory not found at {expected_pages_dir}\nOutput:\n{result.stdout}",
        )

        page1_file: Path = expected_pages_dir / f"{pdf_name_slug}-01.pdf"
        page2_file: Path = expected_pages_dir / f"{pdf_name_slug}-02.pdf"

        self.assertTrue(page1_file.exists())
        self.assertTrue(page2_file.exists())

        doc1 = fitz.open(str(page1_file))
        self.assertIn("CLI Page 1 Text", doc1[0].get_text())
        doc1.close()

        doc2 = fitz.open(str(page2_file))
        self.assertIn("CLI Page 2 Text", doc2[0].get_text())
        doc2.close()


if __name__ == "__main__":
    unittest.main()
