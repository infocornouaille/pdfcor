# Installation

## Installation Standard

```bash
pip install pdfcor
```

### Utilisation de pipx (Recommandé pour l'outil CLI)

Si vous souhaitez utiliser `pdfcor` comme outil en ligne de commande, `pipx` est recommandé car il installe le package dans un environnement isolé et rend ses points d'entrée disponibles globalement.

D'abord, assurez-vous que `pipx` est installé :
```bash
python -m pip install --user pipx
python -m pipx ensurepath
```

Ensuite, installez `pdfcor` avec `pipx` :
```bash
pipx install pdfcor
```
Vous pouvez maintenant exécuter les commandes `pdfcor` directement depuis votre terminal. Pour mettre à jour plus tard : `pipx upgrade pdfcor`.

### Utilisation de uv (Alternative d'installation)

Si vous préférez utiliser `uv` (un installateur de paquets Python rapide), vous pouvez installer `pdfcor` avec :
```bash
uv pip install pdfcor
```
C'est une alternative à l'utilisation de `pip`.

## Dépendances

pdfcor dépend des bibliothèques suivantes :

- PyMuPDF (fitz) : pour l'extraction du contenu des PDF et la manipulation des fichiers PDF
- Pillow (PIL) : pour le traitement des images

Ces dépendances seront automatiquement installées lors de l'installation de `pdfcor` via `pip` (ou l'installateur choisi).
