import os
import sys
import pandas as pd

# Define the season definition as a dictionary
season_definition = {
    'Summer': [6, 7, 8],
    'Autumn': [9, 10, 11],
    'Winter': [12, 1, 2],
    'Spring': [3, 4, 5]
}


# Define a function to map months to seasons
def map_month_to_season(month):
    for season, months in season_definition.items():
        if month in months:
            return season
    return None


# Define a function to get the Timev2 value based on the year and season
def get_timev2(year, season):
    if season == 'Winter':
        return str(year) + '01'
    elif season == 'Spring':
        return str(year) + '04'
    elif season == 'Summer':
        return str(year) + '07'
    elif season == 'Autumn':
        return str(year) + '10'
    else:
        return None


# Main
if __name__ == '__main__':
    data_path = 'C:/Users/justi/Downloads/data_scripts/data_scripts/PM25/month/'
    output_result_path = ''
    result = pd.DataFrame()
    for yyyy in range(2001, 2022):
        for mm in range(1, 13):
            file_name = data_path + str(yyyy * 100 + mm) + '.csv'
            if os.path.isfile(file_name):
                data = pd.read_csv(file_name)
                data['YEAR'] = yyyy
                data.columns = data.columns.str.strip()
                data['Month'] = mm
                data['Season'] = data['Month'].apply(map_month_to_season)
                data = data.groupby(['YEAR', 'TPU', 'Season'], as_index=False)['PM'].mean()
                data['Timev2'] = data.apply(lambda row: get_timev2(row['YEAR'], row['Season']), axis=1)
                data = data.sort_values(by=['TPU'])
                if result.empty:
                    result = data
                else:
                    result = result.append(data)
    print(result)
    result.to_csv(output_result_path + 'seasonal_average_pm25.csv', index=False)
    sys.exit()
