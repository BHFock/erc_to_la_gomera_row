import pandas as pd
from datetime import datetime


def convert_date(date_str):
    date = datetime.strptime(date_str, '%d/%m/%Y')
    return date.strftime('%Y-%m-%d')


csv_path = 'log/ERC land crew log - Sheet1.csv'
log_path = 'log/land_crew.log'

all_data = pd.read_csv(csv_path)
log_data = all_data.iloc[:, 0:3]
log_data['Date'] = log_data['Date'].apply(lambda x: convert_date(x))

log_data.rename(columns={'Date':'date'}, inplace=True)
log_data.rename(columns={'Meters':'meter'}, inplace=True)
log_data.rename(columns={'Name':'name'}, inplace=True)

log_data.to_csv(log_path, index=False, sep=';')
