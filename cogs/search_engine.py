import requests
import spider_configs as sconfig
import pandas as pd
from fuzzywuzzy import fuzz

# Full path
FILE_PATH = sconfig.DATA_PATH + sconfig.CAR_MANUFACTURES

def load_or_create_dataframe( file_path, weblist_url ):
    """Loads or creates a dataframe from the given csv file and url."""
    try:
        df = pd.read_pickle( file_path )
    except FileNotFoundError:
        print( "File Not Found Error. Creating file..." )
        car_manufactures = requests.get( weblist_url ).text.split( "\n" )
        df = pd.DataFrame( car_manufactures, columns=["car_name"])
        df.to_pickle( file_path )

    return df

def match_car_name( car_name ):
    """Returns matched manufacturer name for the given input string using fuzzy matching algorithm with Levenshtein distance."""
    df = load_or_create_dataframe( FILE_PATH, sconfig.CAR_MANUFACTURES_WEBLIST )

    best_match = None
    highest_similarity = -1

    for name in df["car_name"]:
        similarity = fuzz.partial_ratio(car_name.lower(), name.lower())
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = name

    if best_match:
        matched_car_name = best_match
    else:
        weblist_data = requests.get( sconfig.CAR_MANUFACTURES_WEBLIST ).json()
        matched_car_name = weblist_data[0]["name"]
        df = df.append({"car_name": matched_car_name}, ignore_index=True)
        df.to_pickle(FILE_PATH)

    return matched_car_name


