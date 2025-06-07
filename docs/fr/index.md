# Bienvenue sur pdfcor

![Version PyPI](https://img.shields.io/pypi/v/pdfcor.svg)
![Versions Python](https://img.shields.io/pypi/pyversions/pdfcor.svg)

pdfcor est un package Python polyvalent pour travailler avec des fichiers PDF. Il permet d'extraire le contenu en format Markdown avec les images, de fusionner des PDF et d'extraire des pages individuelles.

## Fonctionnalités

- Extraction du contenu textuel des PDF en format Markdown
- Extraction et sauvegarde des images contenues dans les PDF
- Option de traitement récursif des sous-dossiers
- Redimensionnement optionnel des images pour une mise en page A4
- Fusion de plusieurs fichiers PDF en un seul document
- Extraction de pages individuelles d'un PDF
- Utilisable en ligne de commande ou comme module Python
- Messages d'information et d'erreur via le module `logging`

## Fonctionnement

pdfcor offre plusieurs fonctionnalités principales :

1.  **Extraction de contenu en Markdown**:
    - Ouverture du fichier PDF avec PyMuPDF (fitz)
    - Extraction du texte et des images page par page
    - Conversion du texte extrait en format Markdown
    - Sauvegarde des images extraites et insertion des références dans le Markdown

2.  **Fusion de PDF**:
    - Lecture de tous les fichiers PDF dans le dossier spécifié
    - Combinaison de tous les PDF en un seul document
    - Sauvegarde du document fusionné (nom par défaut basé sur le dossier si `--output-file` n'est pas utilisé)

3.  **Extraction de pages**:
    - Ouverture du fichier PDF spécifié
    - Création d'un nouveau PDF pour chaque page
    - Sauvegarde des pages individuelles dans un dossier dédié (nommé `pages-<nom_pdf_slugifie>`) dans le même répertoire que le PDF original.

## Journalisation (Logging)

pdfcor utilise le module `logging` de Python pour afficher les messages d'information et d'erreur. Pour une utilisation en tant que bibliothèque, le comportement du logging peut être personnalisé comme pour toute application Python standard utilisant ce module.
