import pandas as pd
import requests
import uuid
from cleaning_2014 import clean_2014
from cleaning_2022 import clean_2022

# Import des données de 1930 à 2010
df_1930_2010 = pd.read_csv('./data/clean_1930-2010.csv',sep=',')


# Import des données de 2014
data_2014 = pd.read_csv('./data/WorldCup.csv',sep=';',encoding='utf-8-sig')

# Nettoyage des données de 2014
df_2014 = clean_2014(data_2014)

# Import des données de 2018
df_2018 = pd.read_csv('./data/clean_2018.csv')

# Import des données de 2022
url = 'https://worldcupjson.net/matches'
response = requests.get(url)
data_2022 = pd.json_normalize(response.json())

# Nettoyage des données de 2022
df_2022 = clean_2022(data_2022)

# Concaténation des DF
df_matchs = pd.concat([df_1930_2010, df_2014, df_2018, df_2022])
df_matchs['date'] = pd.to_datetime(df_matchs['date']).dt.date 
#df_matchs['id_match'] = [uuid.uuid4() for index, row in df_matchs.iterrows()]
df_matchs = df_matchs.sort_values('date')
df_matchs = df_matchs.reset_index(drop=True)
df_matchs['id_match'] = df_matchs.index + 1
df_matchs.to_csv('./data/all_games.csv',index=False)
print(df_matchs.head(5))