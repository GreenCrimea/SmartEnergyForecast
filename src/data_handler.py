"""
todo
"""
import pandas as pd

wPATHS = [
    "./datasets/weather_melbourne_06.23-05.24/IDCJDW3050.202306.csv",
    "./datasets/weather_melbourne_06.23-05.24/IDCJDW3050.202307.csv",
    "./datasets/weather_melbourne_06.23-05.24/IDCJDW3050.202308.csv",
    "./datasets/weather_melbourne_06.23-05.24/IDCJDW3050.202309.csv",
    "./datasets/weather_melbourne_06.23-05.24/IDCJDW3050.202310.csv",
    "./datasets/weather_melbourne_06.23-05.24/IDCJDW3050.202311.csv",
    "./datasets/weather_melbourne_06.23-05.24/IDCJDW3050.202312.csv",
    "./datasets/weather_melbourne_06.23-05.24/IDCJDW3050.202401.csv",
    "./datasets/weather_melbourne_06.23-05.24/IDCJDW3050.202402.csv",
    "./datasets/weather_melbourne_06.23-05.24/IDCJDW3050.202403.csv",
    "./datasets/weather_melbourne_06.23-05.24/IDCJDW3050.202404.csv",
    "./datasets/weather_melbourne_06.23-05.24/IDCJDW3050.202405.csv",
]



def import_dataset(path, index_col, concat=False, skiprows= False):
    """
    todo
    """
    if not concat:
        return pd.read_csv(path, index_col=index_col, encoding="latin-1")
    frames = []
    for file in path:
        frames.append(pd.read_csv(file, index_col=index_col, encoding="latin-1", skiprows=skiprows))
    return pd.concat(frames, ignore_index=True)

def get_index_cols(path, skiprows = False):
    """
    todo
    """
    with open(path, "r", encoding="latin-1") as file:

        if not skiprows:
            return [data for data in \
                [data.replace('"', '') for data in file.readline().split(",")]\
            if data]

        for idx, lines in enumerate(file):
            if idx == skiprows:
                return [data.replace('\n', '') for data in \
                    [data.replace('"', '') for data in lines.split(",")]\
                if data]

def drop_extra_col(dataframe):
    """
    todo
    """
    return dataframe.drop('Unnamed: 0', axis=1)
