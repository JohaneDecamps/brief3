# World Cup Match Data Pipeline

Ce dépôt contient un pipeline de collecte, nettoyage et ingestion de données de matchs de Coupe du Monde de football dans une base de données MySQL.

## Structure du projet

- Les scripts de récupération / nettoyage des données :
    - `clean_match.ipynb` : nettoyage du fichier `matches.csv` pour les Coupes du Monde de 1930 à 2010 compris.
    - `cleaning_2014.py` : nettoyage du fichier `data/WorldCup.csv` pour la Coupe du Monde 2014.
    - `clean_match2018.ipynb` : nettoyage du json `data_2018.json` pour la Coupe du Monde 2018.
    - `cleaning_2022.py` : nettoyage des données de matchs 2022 issues de l'API `worldcupjson.net`.
- `concat.py` : concatène les fichiers nettoyés et les données 2022 dans `data/all_games.csv`, puis génère un identifiant UUID pour chaque match.
- `ingestion_to_db.py` : crée la table MySQL `matchs` et importe le contenu de `data/all_games.csv`.
- `data/` : contient les fichiers de données bruts et nettoyés.
- `requirements.txt` : dépendances Python requises.

## Prérequis

- Python 3.8+
- MySQL avec un serveur accessible
- Un fichier `.env` avec les variables de connexion à la base de données:
  - `DB_HOST`
  - `DB_USER`
  - `DB_PASSWORD`
  - `DB_PORT`
  - `DB`

Exemple de `.env`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=secret
DB_PORT=3306
DB=worldcup_db
```

## Installation

1. Installer les dépendances :

```bash
pip install -r requirements.txt
```

2. Vérifier que le fichier `.env` est configuré avec les bonnes informations de connexion.

## Utilisation

### 1. Nettoyer et concaténer les données

1. Faire tourner les deux notebooks `clean_match.ipynb` et `clean_match2018.ipynb` pour créer les CSV `clean_[date].csv`
2. Lancer le script `concat.py` :
    - lit les CSV `data/clean_1930-2010.csv` et `data/clean_2018.csv`
    - nettoie `data/WorldCup.csv` via `cleaning_2014.py`
    - récupère et nettoie les données 2022 via `cleaning_2022.py`
    - assemble toutes les lignes dans `data/all_games.csv`

```bash
python concat.py
```

### 2. Créer la table MySQL et importer les données

Le script `ingestion_to_db.py` :
- se connecte à MySQL
- crée la table `matchs` si elle n'existe pas
- importe les lignes de `data/all_games.csv`

```bash
python ingestion_to_db.py
```

## Schéma de la table `matchs`

- `id_match` : CHAR(36)
- `home_team` : VARCHAR(255)
- `away_team` : VARCHAR(255)
- `home_result` : INT
- `away_result` : INT
- `result` : VARCHAR(255)
- `date` : DATE
- `round` : VARCHAR(255)
- `city` : VARCHAR(255)
- `edition` : VARCHAR(255)

## Notes

- Le script `concat.py` utilise une colonne `id_match` générée avec `uuid.uuid4()`.
- `ingestion_to_db.py` utilise `INSERT IGNORE` pour éviter les doublons sur les clés primaires.
- Si la table existe déjà, le script ne la recrée pas et continue avec l'import des données.
