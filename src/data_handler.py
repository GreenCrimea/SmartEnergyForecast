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

wPATHS2 = [
    "./datasets/BOM_year.csv"
]

hPATHS = [
    "../datasets/House 3_Melb East.csv",
    "../datasets/House 4_Melb West.csv",
    "../datasets/House 4_Solar.csv",
]



def import_dataset(path, index_col, concat=False, skiprows= False):
    """
    todo
    """
    if not concat:
        return pd.read_csv(path[0], index_col=index_col, encoding="latin-1")
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

def prepare_house_data():

    data = pd.read_csv("./datasets/House 3_Melb East.csv", index_col=False, encoding="latin-1", names=["datetime", "values"])
    data["datetime"] = pd.to_datetime(data['datetime'], format='%Y-%m-%d %H:%M:%S')
    data["date"] = data["datetime"].dt.date
    
    daily_mean = data.groupby('date')['values'].mean().reset_index().rename(columns={'values': 'house3_average'})
    daily_max = data.groupby('date')['values'].max().reset_index().rename(columns={'values': 'house3_max'})
    daily_min = data.groupby('date')['values'].min().reset_index().rename(columns={'values': 'house3_min'})
    daily_median = data.groupby('date')['values'].median().reset_index().rename(columns={'values': 'house3_median'})

    start_date = pd.to_datetime('2023-03-01').date()
    end_date = pd.to_datetime('2024-04-17').date()

    filtered_mean = daily_mean[(daily_mean['date'] >= start_date) & (daily_mean['date'] <= end_date)]
    filtered_max = daily_max[(daily_max['date'] >= start_date) & (daily_max['date'] <= end_date)]
    filtered_min = daily_min[(daily_min['date'] >= start_date) & (daily_min['date'] <= end_date)]
    filtered_median = daily_median[(daily_median['date'] >= start_date) & (daily_median['date'] <= end_date)]

    merged_df = pd.merge(filtered_mean, filtered_max, on='date', suffixes=('_house3_mean', '_house3_max'))
    merged_df = pd.merge(merged_df, filtered_min, on='date', suffixes=('', '_house3_min'))
    merged_df = pd.merge(merged_df, filtered_median, on='date', suffixes=('', '_house3_median'))

    house3 = merged_df

    data = pd.read_csv("./datasets/House 4_Melb West.csv", index_col=False, encoding="latin-1", names=["datetime", "values"])
    data["datetime"] = pd.to_datetime(data['datetime'], format='%Y-%m-%d %H:%M:%S')
    data["date"] = data["datetime"].dt.date
    
    daily_mean = data.groupby('date')['values'].mean().reset_index().rename(columns={'values': 'house4_average'})
    daily_max = data.groupby('date')['values'].max().reset_index().rename(columns={'values': 'house4_max'})
    daily_min = data.groupby('date')['values'].min().reset_index().rename(columns={'values': 'house4_min'})
    daily_median = data.groupby('date')['values'].median().reset_index().rename(columns={'values': 'house4_median'})

    start_date = pd.to_datetime('2023-03-01').date()
    end_date = pd.to_datetime('2024-04-17').date()

    filtered_mean = daily_mean[(daily_mean['date'] >= start_date) & (daily_mean['date'] <= end_date)]
    filtered_max = daily_max[(daily_max['date'] >= start_date) & (daily_max['date'] <= end_date)]
    filtered_min = daily_min[(daily_min['date'] >= start_date) & (daily_min['date'] <= end_date)]
    filtered_median = daily_median[(daily_median['date'] >= start_date) & (daily_median['date'] <= end_date)]

    merged_df = pd.merge(filtered_mean, filtered_max, on='date', suffixes=('_house4_mean', '_house4_max'))
    merged_df = pd.merge(merged_df, filtered_min, on='date', suffixes=('', '_house4_min'))
    merged_df = pd.merge(merged_df, filtered_median, on='date', suffixes=('', '_house4_median'))

    house4 = merged_df

    data = pd.read_csv("./datasets/House 4_Solar.csv", index_col=False, encoding="latin-1", names=["datetime", "values"])
    data["datetime"] = pd.to_datetime(data['datetime'], format='%d/%m/%Y %H:%M')
    data["date"] = data["datetime"].dt.date
    
    daily_mean = data.groupby('date')['values'].mean().reset_index().rename(columns={'values': 'house3solar_average'})
    daily_max = data.groupby('date')['values'].max().reset_index().rename(columns={'values': 'house3solar_max'})
    daily_min = data.groupby('date')['values'].min().reset_index().rename(columns={'values': 'house3solar_min'})
    daily_median = data.groupby('date')['values'].median().reset_index().rename(columns={'values': 'house3solar_median'})

    start_date = pd.to_datetime('2023-03-01').date()
    end_date = pd.to_datetime('2024-04-17').date()

    filtered_mean = daily_mean[(daily_mean['date'] >= start_date) & (daily_mean['date'] <= end_date)]
    filtered_max = daily_max[(daily_max['date'] >= start_date) & (daily_max['date'] <= end_date)]
    filtered_min = daily_min[(daily_min['date'] >= start_date) & (daily_min['date'] <= end_date)]
    filtered_median = daily_median[(daily_median['date'] >= start_date) & (daily_median['date'] <= end_date)]

    merged_df = pd.merge(filtered_mean, filtered_max, on='date', suffixes=('_house3solar_mean', '_house3solar_max'))
    merged_df = pd.merge(merged_df, filtered_min, on='date', suffixes=('', '_house3solar_min'))
    merged_df = pd.merge(merged_df, filtered_median, on='date', suffixes=('', '_house3solar_median'))

    house4solar = merged_df

    merged_data = pd.merge(house3, house4, on="date")
    merged_data = pd.merge(merged_data, house4solar, on="date")

    merged_data.to_csv('./datasets/houses_daily_statistics.csv', index=False)



prepare_house_data()
