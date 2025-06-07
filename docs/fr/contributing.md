# Contribuer à pdfcor

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une "issue" (problème/demande) ou à soumettre une "pull request" (demande de fusion) sur notre dépôt GitHub.

## Configuration de l'Environnement de Développement

Nous utilisons `uv` pour gérer les environnements virtuels et les dépendances durant le développement.

1.  **Clonez le dépôt**:
    ```bash
    git clone https://github.com/infocornouaille/pdfcor.git # Remplacez par l'URL réelle du dépôt si différente
    cd pdfcor
    ```

2.  **Créez et activez un environnement virtuel**:
    ```bash
    # Installez uv si vous ne l'avez pas déjà fait : https://github.com/astral-sh/uv#installation
    uv venv .venv
    source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate
    ```

3.  **Installez les dépendances (y compris les outils de développement comme Ruff)**:
    ```bash
    uv pip install -e .[dev]
    ```
Ceci installe le package en mode éditable (`-e`) avec les dépendances optionnelles `dev` spécifiées dans `pyproject.toml`.

## Style de Code et Qualité

Ce projet utilise [Ruff](https://github.com/astral-sh/ruff) pour le "linting" (analyse statique du code) et le formatage du code (style compatible Black).
Après avoir configuré votre environnement de développement, vous pouvez formater et vérifier votre code en exécutant :

```bash
# Formater le code
ruff format .

# Vérifier les problèmes de linting (et en corriger certains automatiquement)
ruff check --fix .
```

Un workflow GitHub Actions est également en place pour vérifier automatiquement le formatage du code et le linting lors des "pushes" et "pull requests".
Veuillez vous assurer que vos contributions passent ces vérifications.

## Exécution des Tests

Pour exécuter les tests unitaires :
```bash
python -m unittest discover tests
```
Ou, si votre environnement virtuel est activé :
```bash
unittest discover tests
```
Assurez-vous que tous les tests passent avant de soumettre vos contributions.

## Compilation et Publication

Ce projet utilise [Hatchling](https://hatch.pypa.io/latest/) comme backend de compilation, tel que défini dans `pyproject.toml`.

### Compilation du Package

1.  Assurez-vous d'avoir le package `build` installé :
    ```bash
    uv pip install build  # Ou : python -m pip install build
    ```
2.  Exécutez la commande de compilation depuis la racine du projet :
    ```bash
    python -m build
    ```
    Ceci créera les fichiers `sdist` et `wheel` dans le répertoire `dist/`.

### Publication sur PyPI (Localement)

La publication est généralement effectuée par les mainteneurs du projet.

1.  Assurez-vous d'avoir `twine` installé :
    ```bash
    uv pip install twine  # Ou : python -m pip install twine
    ```
2.  Téléversez les distributions depuis le répertoire `dist/` :
    ```bash
    twine upload dist/*
    ```
    Vous serez invité à entrer votre nom d'utilisateur et mot de passe PyPI. Il est recommandé d'utiliser des jetons d'API (API tokens) avec Twine.

## Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` à la racine du dépôt pour plus de détails.
