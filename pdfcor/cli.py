import argparse
import os
from .core import process_folder


def main():
    parser = argparse.ArgumentParser(
        description="Extraire le contenu des PDF en Markdown avec images."
    )
    parser.add_argument(
        "--input-folder", default=".", help="Dossier d'entrée contenant les PDF"
    )
    parser.add_argument(
        "--output-folder",
        help="Dossier de sortie pour les fichiers Markdown et les images",
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

    args = parser.parse_args()

    input_folder = os.path.abspath(args.input_folder)
    output_folder = (
        os.path.abspath(args.output_folder) if args.output_folder else input_folder
    )

    process_folder(input_folder, output_folder, args.recursive, args.resize)


if __name__ == "__main__":
    main()
