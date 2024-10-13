# pdfcor

![PyPI version](https://img.shields.io/pypi/v/pdfcor.svg)
![Python versions](https://img.shields.io/pypi/pyversions/pdfcor.svg)

pdfcor est un package Python polyvalent pour travailler avec des fichiers PDF. Il permet d'extraire le contenu en format Markdown avec les images, de fusionner des PDF et d'extraire des pages individuelles.

## Installation

```
pip install pdfcor
```

## Dépendances

pdfcor dépend des bibliothèques suivantes :

- PyMuPDF (fitz) : pour l'extraction du contenu des PDF et la manipulation des fichiers PDF
- Pillow (PIL) : pour le traitement des images

Ces dépendances seront automatiquement installées lors de l'installation de pdfcor via pip.

## Utilisation

pdfcor peut être utilisé en ligne de commande avec diverses options :

### Extraction de contenu en Markdown

```
pdfcor --input-folder <dossier_entree> --output-folder <dossier_sortie> [--recursive] [--resize]
```

#### Options

- `--input-folder` : Spécifie le dossier d'entrée contenant les fichiers PDF à traiter. Par défaut, il utilise le dossier courant.
- `--output-folder` : Définit le dossier de sortie pour les fichiers Markdown et les images extraites. Si non spécifié, il utilise le même dossier que l'entrée.
- `--recursive` : Active le traitement récursif des sous-dossiers.
- `--resize` : Redimensionne les images extraites pour qu'elles tiennent sur une page A4.

### Fusion de PDF

```
pdfcor --fusion [--input-folder <dossier_entree>] [--output <nom_fichier_sortie>]
```

Cette commande fusionne tous les PDF d'un dossier sans aucune transformation.

#### Options

- `--input-folder` : Spécifie le dossier contenant les PDF à fusionner. Par défaut, utilise le dossier courant.
- `--output` : Spécifie le nom du fichier PDF fusionné. Par défaut, utilise le nom du dossier d'entrée.

### Extraction de pages

```
pdfcor --pages <fichier_pdf>
```

Cette commande extrait toutes les pages d'un PDF dans des fichiers séparés.

#### Options

- `<fichier_pdf>` : Le fichier PDF dont vous voulez extraire les pages.

## Exemples

1. Extraire le contenu de tous les PDF dans le dossier courant :
   ```
   pdfcor
   ```

2. Fusionner tous les PDF d'un dossier :
   ```
   pdfcor --fusion --input-folder /chemin/vers/pdfs
   ```

3. Extraire les pages d'un PDF spécifique :
   ```
   pdfcor --pages example.pdf
   ```

## Utilisation comme module Python

Vous pouvez également utiliser pdfcor comme module dans vos scripts Python :

```python
from pdfcor import process_pdf, process_folder, merge_pdfs, extract_pages

# Traiter un seul fichier PDF
process_pdf("/chemin/vers/fichier.pdf", "/chemin/vers/sortie", resize=False)

# Traiter un dossier entier
process_folder("/chemin/vers/dossier", "/chemin/vers/sortie", recursive=True, resize=True)

# Fusionner des PDF
merge_pdfs("/chemin/vers/dossier", "fichier_fusionne.pdf")

# Extraire les pages d'un PDF
extract_pages("/chemin/vers/fichier.pdf")
```

## Fonctionnalités

- Extraction du contenu textuel des PDF en format Markdown
- Extraction et sauvegarde des images contenues dans les PDF
- Option de traitement récursif des sous-dossiers
- Redimensionnement optionnel des images pour une mise en page A4
- Fusion de plusieurs fichiers PDF en un seul document
- Extraction de pages individuelles d'un PDF
- Utilisable en ligne de commande ou comme module Python

## Fonctionnement

pdfcor offre plusieurs fonctionnalités principales :

1. Extraction de contenu en Markdown :
   - Ouverture du fichier PDF avec PyMuPDF (fitz)
   - Extraction du texte et des images page par page
   - Conversion du texte extrait en format Markdown
   - Sauvegarde des images extraites et insertion des références dans le Markdown

2. Fusion de PDF :
   - Lecture de tous les fichiers PDF dans le dossier spécifié
   - Combinaison de tous les PDF en un seul document
   - Sauvegarde du document fusionné avec le nom du dossier par défaut

3. Extraction de pages :
   - Ouverture du fichier PDF spécifié
   - Création d'un nouveau PDF pour chaque page
   - Sauvegarde des pages individuelles dans un dossier dédié

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request sur notre dépôt GitHub.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.