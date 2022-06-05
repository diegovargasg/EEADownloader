# importing csv module
import pandas as pd
 
# csv file name
filename = "DE_5_71718_2020_timeseries.csv"

# read file
df = pd.read_csv(filename)

# convert to datetime
df['DatetimeBegin'] = pd.to_datetime(df['DatetimeBegin'])

# calculate mask
mask = df['DatetimeBegin'].between('2020-04-01', '2020-04-30')

# output masked dataframes
df[~mask].to_csv('out1.csv', index=False)
df[mask].to_csv('out2.csv', index=False)