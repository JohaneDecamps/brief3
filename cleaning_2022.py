import pandas as pd
import requests

url = 'https://worldcupjson.net/matches'

response = requests.get(url)
data = pd.json_normalize(response.json())
print(data.stage_name.unique())

def clean_2022(data) :
    # Normalisation de datetime au format YYYYMMDD :
    data['datetime'] = pd.to_datetime(data['datetime']).dt.strftime("%Y%m%d")

    # Création de result :
    data.loc[data['winner'] == 'Draw', 'result'] = 'draw'
    data.loc[data['winner_code'] == data['home_team_country'], 'result'] = 'home_team'
    data.loc[data['winner_code'] == data['away_team_country'], 'result'] = 'away_team'
    
    # Normalisation des Rounds
    data.loc[data['stage_name'] == 'First stage','stage_name'] = 'Poules'
    data.loc[data['stage_name'] == 'Round of 16','stage_name'] = 'Huitièmes de finale'
    data.loc[data['stage_name'] == 'Quarter-final','stage_name'] = 'Quarts de finale'
    data.loc[data['stage_name'] == 'Semi-final','stage_name'] = 'Demi-finales'
    data.loc[data['stage_name'] == 'Play-off for third place','stage_name'] = 'Troisième place'
    data.loc[data['stage_name'] == 'Final','stage_name'] = 'Finale'
    return pd.DataFrame({
        'id_match':data['id'],
        'home_team': data['home_team.name'],
        'away_team': data['away_team.name'],
        'home_result': data['home_team.goals'],
        'away_result': data['away_team.goals'],
        'result': data['result'],
        'date': data['datetime'],
        'round': data['stage_name'],
        'city': data['location'],
        'edition': 2024
    }).sort_values(['date','id_match'])