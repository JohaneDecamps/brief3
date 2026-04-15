import pandas as pd

data = pd.read_csv('./data/WorldCup.csv',sep=';',encoding='utf-8-sig')

def clean_2014(data) :
    # Certains matchs en double, on les supprime :
    data = data.drop_duplicates()

    # Nettoyage des noms de pays :
    data['Home Team Name'] = data['Home Team Name'].str.replace('C�te', 'Côte')
    data['Away Team Name'] = data['Away Team Name'].str.replace('C�te', 'Côte')
    data['Home Team Name'] = data['Home Team Name'].str.replace('rn">Bosnia ', 'Bosnia')
    data['Away Team Name'] = data['Away Team Name'].str.replace('rn">Bosnia ', 'Bosnia')
    
    # Normalisation de la date au format YYYYMMDD :
    data['Datetime'] = pd.to_datetime(data['Datetime']).dt.strftime("%Y%m%d")

    # Création de la colonne résultat
    data['result'] = 'draw'
    data.loc[data['Home Team Goals'] > data['Away Team Goals'], 'result']= 'home_team'
    data.loc[data['Home Team Goals'] < data['Away Team Goals'], 'result']= 'away_team'

    # Normalisation des Rounds
    data.loc[data['Stage'].str.startswith('Group'),'Stage'] = 'Poules'
    data.loc[data['Stage'] == 'Round of 16','Stage'] = 'Huitièmes de finale'
    data.loc[data['Stage'] == 'Quarter-finals','Stage'] = 'Quarts de finale'
    data.loc[data['Stage'] == 'Semi-finals','Stage'] = 'Demi-finales'
    data.loc[data['Stage'] == 'Play-off for third place','Stage'] = 'Troisième place'
    data.loc[data['Stage'] == 'Final','Stage'] = 'Finale'

    return pd.DataFrame({
        'id_match':data['MatchID'],
        'home_team': data['Home Team Name'],
        'away_team': data['Away Team Name'],
        'home_result': data['Home Team Goals'],
        'away_result': data['Away Team Goals'],
        'result': data['result'],
        'date': data['Datetime'],
        'round': data['Stage'],
        'city': data['City'],
        'edition': data['Year']
    }).sort_values(['date','id_match'])
