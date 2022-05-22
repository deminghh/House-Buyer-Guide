import requests
import os
import pandas as pd
from IPython.core.display import HTML
import json
from cred import credentials


# define a function to request the Genesis API 
def get_genesis_api(
        code: str,
        years: list[int],
        skiprows: int=4,
        skipfooter: int=4,
        delimiter: str=';',
        header: list[int]=[0,1],
        save_json: bool=False,
) -> pd.DataFrame:

    dataframes = {}
    for year in years:
        de_request_url = f'https://www-genesis.destatis.de/genesisWS/rest/2020/data/table'
        de_request_params = {
            'username': credentials['username'],
            'password': credentials['password'],
            "name": code,  # e.g. "12411-0014" the population per state, sex, nationality
            "area": "all",
            "compress": "false",
            "transpose": "false",
            "startyear": year,
            "endyear": year,
            "timeslices": "",
            "regionalvariable": "",
            "regionalkey": "",
            "classifyingvariable1": "",
            "classifyingkey1": "",
            "classifyingvariable2": "",
            "classifyingkey2": "",
            "classifyingvariable3": "",
            "classifyingkey3": "",
            "job": "false",
            "stand": "01.01.1970",
            "language": "en" ,
        }
        # to save the response as json in a file called "r_population_kries_year.json"
        de_response = requests.get(url=de_request_url, params=de_request_params)
        if save_json:
            with open(f'data/{code}_{year}.json', 'w') as f:
                json.dump(de_response.json(), f, indent=2)

        # to save the part of response (the table) as a csv called "r_population_kreis_year.csv" 
        with open(f'data/{code}_{year}.csv', 'w') as csv_file:
            csv_file.write(de_response.json()['Object']['Content'])

        dataframes[year] = pd.read_csv(f'data/{code}_{year}.csv',
            skiprows=skiprows, skipfooter=skipfooter, delimiter=delimiter, header=header, engine='python')  
    
    result = pd.concat(dataframes.values(), axis=0)
    if max(years) != min(years):
        print('Dumping concatenated DF')
        result.to_csv(f'data/{code}_{min(years)}_{max(years)}.csv')

    return result

