import argparse
import os
from .core import process_folder, merge_pdfs, extract_pages
# import sys # For printing sys.argv # No longer needed


def main():
    # print(f"CLI main invoked. sys.argv: {sys.argv}", file=sys.stderr) # Debug print removed
    parser = argparse.ArgumentParser(
        description="Extraire le contenu des PDF en Markdown avec images."
    )
    parser.add_argument(
        "--input-folder", default=".", help="Dossier d'entrée contenant les PDF ou pour la fusion"
    )
    parser.add_argument(
        "--output-folder",
        help="Dossier de sortie pour les fichiers Markdown et les images. Défaut: 'pdfcor_output' dans le dossier d'entrée.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Traiter récursivement les sous-dossiers",
    )
    parser.add_argument(
        "--resize",
        action="store_true",
        help="Redimensionner les images pour tenir sur une page A4",
    )
    parser.add_argument(
        "--fusion",
        action="store_true",
        help="Fusionner tous les PDF du dossier d'entrée",
    )
    parser.add_argument(
        "--output-file", help="Nom du fichier PDF fusionné (ex: merged.pdf) ou chemin complet."
    )
    parser.add_argument(
        "--pages",
        help="Extraire les pages du PDF spécifié",
    )

    args = parser.parse_args()
    # print(f"CLI parsed args: {args}", file=sys.stderr) # Debug print removed

    input_folder = os.path.abspath(args.input_folder) # Defines input_folder for all operations
    # print(f"CLI input_folder (abs): {input_folder}", file=sys.stderr) # Debug print removed

    if args.fusion:
        # print("CLI mode: fusion", file=sys.stderr) # Debug print removed
        if args.output_file:
            user_output_path = args.output_file # Can be "name.pdf", "some/dir/name.pdf", or "some/dir/"

            final_output_filename = os.path.basename(user_output_path)
            final_output_dir_str = os.path.dirname(user_output_path)

            if not final_output_filename: # User provided "some/dir/"
                final_output_filename = None # Let merge_pdfs decide the name
                final_output_dir = os.path.abspath(final_output_dir_str if final_output_dir_str else user_output_path) # Use the full path as dir
            elif not final_output_dir_str: # User provided "name.pdf"
                final_output_dir = None # merge_pdfs will use input_folder
            else: # User provided "some/dir/name.pdf"
                final_output_dir = os.path.abspath(final_output_dir_str)

            # print(f"CLI fusion params: input_folder={input_folder}, output_file={final_output_filename}, output_dir={final_output_dir}", file=sys.stderr) # Debug print removed
            merge_pdfs(input_folder, output_file=final_output_filename, output_dir=final_output_dir)
        else:
            # print(f"CLI fusion params (default output): input_folder={input_folder}", file=sys.stderr) # Debug print removed
            merge_pdfs(input_folder, output_file=None, output_dir=None)
    elif args.pages:
        # Ensure pages path is absolute if not already, or handle as needed by extract_pages
        # print(f"CLI mode: pages, pdf_path={args.pages}", file=sys.stderr) # Debug print removed
        pages_pdf_path = os.path.abspath(args.pages)
        extract_pages(pages_pdf_path) # extract_pages handles its own output dir logic relative to pdf_path

    else:
        # print(f"CLI mode: process_folder (markdown)", file=sys.stderr) # Debug print removed
        # This is for process_folder (Markdown extraction)
        if args.output_folder is None:
            # Default output is 'pdfcor_output' inside the absolute input_folder
            output_folder_to_use = os.path.join(input_folder, "pdfcor_output")
        else:
            output_folder_to_use = os.path.abspath(args.output_folder)

        # print(f"CLI process_folder params: input_folder={input_folder}, output_folder_to_use={output_folder_to_use}, recursive={args.recursive}, resize={args.resize}", file=sys.stderr) # Debug print removed
        os.makedirs(output_folder_to_use, exist_ok=True) # Ensure the output folder exists
        process_folder(input_folder, output_folder_to_use, args.recursive, args.resize)


if __name__ == "__main__":
    main()
