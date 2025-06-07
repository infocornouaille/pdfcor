# Guide d'utilisation

## Interface en Ligne de Commande (CLI)

pdfcor peut être utilisé depuis la ligne de commande avec diverses options, structurées en commandes.

### Traitement des PDF en Markdown

Commande : `pdfcor process [OPTIONS]`

(Exemple : `pdfcor process --input-folder <dossier_entree> --output-folder <dossier_sortie> [--recursive] [--resize]`)

**Options**:

- `--input-folder`: Spécifie le dossier d'entrée contenant les fichiers PDF à traiter. Par défaut, utilise le répertoire courant.
- `--output-folder`: Définit le dossier de sortie pour les fichiers Markdown et les images extraites. Si non spécifié, utilise un sous-dossier nommé `pdfcor_output` dans le dossier d'entrée.
- `--recursive` / `-r`: Active le traitement récursif des sous-dossiers.
- `--resize`: Redimensionne les images extraites pour qu'elles tiennent sur une page A4.

### Fusion de PDF

Commande : `pdfcor merge [OPTIONS]`

(Exemple : `pdfcor merge --input-folder <dossier_entree> --output-file <nom_fichier_ou_chemin_sortie>`)

Cette commande fusionne tous les PDF d'un dossier sans aucune transformation.

**Options**:

- `--input-folder`: Spécifie le dossier contenant les PDF à fusionner. Par défaut, utilise le répertoire courant.
- `--output-file`: Spécifie le nom et/ou le chemin du fichier PDF fusionné.
    - Si seul un nom est fourni (ex: `mon_fichier.pdf`), le PDF fusionné sera sauvegardé dans le dossier d'entrée (`--input-folder`).
    - Si un chemin complet est fourni (ex: `/un/autre/dossier/mon_fichier.pdf`), il sera sauvegardé à cet emplacement.
    - Si cette option n'est pas utilisée, le fichier fusionné sera nommé d'après le dossier d'entrée (ex: `nom_dossier_entree.pdf`) et sauvegardé dans ce même dossier d'entrée.

### Extraction de Pages

Commande : `pdfcor extract <fichier_pdf>`

Cette commande extrait toutes les pages d'un PDF dans des fichiers séparés.

**Arguments**:

- `<fichier_pdf>`: Le fichier PDF duquel vous voulez extraire les pages. (Requis)

## Exemples CLI

1.  **Extraire le contenu de tous les PDF dans le répertoire courant** (sortie dans `./pdfcor_output`):
    ```bash
    pdfcor process
    ```
    (Si `--input-folder` n'est pas spécifié, il utilise par défaut le répertoire courant. Si `--output-folder` n'est pas spécifié, il utilise par défaut `pdfcor_output` à l'intérieur du dossier d'entrée.)

2.  **Fusionner tous les PDF d'un dossier**, en spécifiant le nom et l'emplacement du fichier fusionné :
    ```bash
    pdfcor merge --input-folder /chemin/vers/pdfs --output-file /chemin/vers/autre_dossier/fusion.pdf
    ```
    Pour sauvegarder dans le dossier d'entrée avec un nom spécifique :
    ```bash
    pdfcor merge --input-folder /chemin/vers/pdfs --output-file fusion_locale.pdf
    ```

3.  **Extraire les pages d'un PDF spécifique**:
    ```bash
    pdfcor extract example.pdf
    ```

## Utilisation comme Module Python

Vous pouvez également utiliser pdfcor comme module dans vos scripts Python :

```python
from pdfcor import process_pdf, process_folder, merge_pdfs, extract_pages
from pathlib import Path # Assurez-vous d'importer Path
from typing import Optional # Pour les types optionnels

# Traiter un seul fichier PDF
# process_pdf(pdf_path: Path, output_dir: Path, resize: bool = False)
process_pdf(Path("/chemin/vers/fichier.pdf"), Path("/chemin/vers/sortie"), resize=False)

# Traiter un dossier entier
# process_folder(folder_path: Path, output_dir: Path, recursive: bool = False, resize: bool = False)
process_folder(Path("/chemin/vers/dossier"), Path("/chemin/vers/sortie"), recursive=True, resize=True)

# Fusionner des PDF
# merge_pdfs(input_folder: Path, output_file: Optional[str] = None, output_dir: Optional[Path] = None)
merge_pdfs(Path("/chemin/vers/dossier"), output_file="fichier_fusionne.pdf") # Sauvegarde fichier_fusionne.pdf dans /chemin/vers/dossier

# Extraire les pages d'un PDF
# extract_pages(pdf_path: Path)
extract_pages(Path("/chemin/vers/fichier.pdf"))
```
Note : Les fonctions principales attendent maintenant des objets `pathlib.Path` pour les arguments de chemin.
