# pdfcor

pdfcor est un package Python conçu pour extraire le contenu des fichiers PDF et le convertir en format Markdown avec les images incluses.

## Installation

```
pip install pdfcor
```

## Dépendances

pdfcor dépend des bibliothèques suivantes :

- PyMuPDF (fitz) : pour l'extraction du contenu des PDF
- Pillow (PIL) : pour le traitement des images

Ces dépendances seront automatiquement installées lors de l'installation de pdfcor via pip.

## Utilisation

### En ligne de commande

pdfcor peut être utilisé en ligne de commande avec diverses options :

```
pdfcor --input-folder <dossier_entree> --output-folder <dossier_sortie> [--recursive] [--resize]
```

#### Options

- `--input-folder` : Spécifie le dossier d'entrée contenant les fichiers PDF à traiter. Par défaut, il utilise le dossier courant.
- `--output-folder` : Définit le dossier de sortie pour les fichiers Markdown et les images extraites. Si non spécifié, il utilise le même dossier que l'entrée.
- `--recursive` : Active le traitement récursif des sous-dossiers.
- `--resize` : Redimensionne les images extraites pour qu'elles tiennent sur une page A4.

#### Exemples

1. Traiter tous les PDF dans le dossier courant :
   ```
   pdfcor
   ```

2. Traiter les PDF d'un dossier spécifique et sauvegarder les résultats ailleurs :
   ```
   pdfcor --input-folder /chemin/vers/pdfs --output-folder /chemin/vers/sortie
   ```

3. Traiter récursivement tous les PDF et redimensionner les images :
   ```
   pdfcor --input-folder /chemin/vers/pdfs --recursive --resize
   ```

### Comme module Python

Vous pouvez également utiliser pdfcor comme module dans vos scripts Python :

```python
from pdfcor import process_pdf, process_folder

# Traiter un seul fichier PDF
process_pdf("/chemin/vers/fichier.pdf", "/chemin/vers/sortie", resize=False)

# Traiter un dossier entier
process_folder("/chemin/vers/dossier", "/chemin/vers/sortie", recursive=True, resize=True)
```

## Fonctionnalités

- Extraction du contenu textuel des PDF en format Markdown
- Extraction et sauvegarde des images contenues dans les PDF
- Option de traitement récursif des sous-dossiers
- Redimensionnement optionnel des images pour une mise en page A4
- Utilisable en ligne de commande ou comme module Python

## Fonctionnement

pdfcor fonctionne de la manière suivante :

1. Ouverture du fichier PDF avec PyMuPDF (fitz).
2. Extraction du texte page par page, en préservant la structure des blocs de texte.
3. Identification et extraction des images de chaque page.
4. Conversion du texte extrait en format Markdown.
5. Sauvegarde des images extraites dans un sous-dossier dédié.
6. Insertion des références aux images dans le fichier Markdown.
7. Si l'option de redimensionnement est activée, les images sont redimensionnées pour tenir sur une page A4.
8. Le fichier Markdown final est sauvegardé, contenant le texte et les références aux images.

Ce processus est répété pour chaque fichier PDF dans le dossier d'entrée, et dans les sous-dossiers si l'option récursive est activée.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request sur notre dépôt GitHub.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.