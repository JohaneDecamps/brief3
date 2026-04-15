import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
import pandas as pd

# Chargement des variables d'environnement
load_dotenv()

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
port = os.getenv('DB_PORT')
db = os.getenv('DB')

# Création de la connexion avec MySQL Server
try :
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=int(port),
        db=db
    )
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Accès refusé, username ou password incorrect")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("La DB n'exsite pas")
  else:
    print(err)

### Création de la table
# Requête CREATE TABLE
table = (
    "CREATE TABLE `matchs` ("
    "  `id_match` CHAR(36),"
    "  `home_team` VARCHAR(255),"
    "  `away_team` VARCHAR(255),"
    "  `home_result` INT,"
    "  `away_result` INT,"
    "  `result` VARCHAR(255),"
    "  `date` DATE,"
    "  `round` VARCHAR(255),"
    "  `city` VARCHAR(255),"
    "  `edition` VARCHAR(255),"
    "  PRIMARY KEY (`id_match`)"
    ") ENGINE=InnoDB")

cursor = conn.cursor()
# Exécution de la requête
try:
    cursor.execute(table)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("La table existe déjà")
    else:
        print(err.msg)
else:
    print("OK")
    conn.commit()


### Ingestion des données
# Import du CSV
df = pd.read_csv('./data/all_games.csv')
# Mise en forme
data = [(
            row['id_match'],
            row['home_team'],
            row['away_team'],
            row['home_result'],
            row['away_result'],
            row['result'],
            row['date'],
            row['round'],
            row['city'],
            row['edition']) for _, row in df.iterrows()]
# Syntaxe de la requête
req = "INSERT IGNORE INTO matchs (id_match, home_team, away_team, home_result, away_result, result," \
      "date, round, city, edition) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# Exécution de la requête pour réaliser l'import en masse des nouvelles lignes
cursor.executemany(req, data)
conn.commit()

cursor.close()
conn.close()