# importing csv module
import pandas as pd
import os
import glob

year="2019"
 
path = year+"_csv"
allFiles = glob.glob(os.path.join(path, "*.csv"))

for pFile in allFiles:
    fileName = pFile.split('\\')[-1]
    print("Ready to filter "+fileName)

    # read file
    dataFrame = pd.read_csv(pFile)

    # # convert to datetime
    dataFrame['DatetimeBegin'] = pd.to_datetime(dataFrame['DatetimeBegin'])

    # # calculate mask
    mask = dataFrame['DatetimeBegin'].between(year+'-04-01', year+'-04-30')

    # # output masked dataframes
    dataFrame[mask].to_csv(year+"_csv_april_filtered/"+fileName+"_filtered.csv", index=False)
    print("Done with filter "+fileName)



#### Calculates the average per point

path = year+"_csv_april_filtered"
allFilteredFiles = glob.glob(os.path.join(path, "*.csv"))

for pFile in allFilteredFiles:
    # get file name
    fileName = pFile.split('\\')[-1]

    # read file
    dataFrame = pd.read_csv(pFile)

    # Calculate mask
    newDataFrame = dataFrame.groupby(['AirQualityStation', 'UnitOfMeasurement'])['Concentration'].agg(['mean']).reset_index()

    #calculate mean concentration
    newDataFrame.to_csv(year+"_csv_mean_concentration/"+fileName+"_mean_concentration.csv", index=False)
    print("saves mean concentration for "+fileName)


#### concatenates all filtered files

path = year+"_csv_mean_concentration"
allFilteredFiles = glob.glob(os.path.join(path, "*.csv"))

for pFile in allFilteredFiles:
    print("Concatenates "+pFile.split('\\')[-1])
    dataFrame = pd.concat((pd.read_csv(f) for f in allFilteredFiles))

dataFrame.to_csv(year+"_csv_single_file_filtered/csv_filtered.csv", index=False)