# Import des images du trombi UTT

Les images du trombi UTT sont protégées derrière le CAS.

Cet algo va

1. vous demander vos identifiants CAS
2. se connecter au site etu et récupérer la liste de tous les utilisateurs
3. Récupérer pour chacun d'entre eux leur photo de profil et la placer dans le dossier de votre choix

## Usage

1. `cp .env.dist .env && nano .env`
2. `pip install --upgrade pipenv`
3. `pipenv run python algo.py`