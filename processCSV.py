# importing csv module
import pandas as pd
import os
import glob

year="2022"



#### Filters the date by april

path = year+"_csv"
allFiles = glob.glob(os.path.join(path, "*.csv"))
totalLenFiles = len(allFiles)
countFilesProccessed = 1

for pFile in allFiles:
    fileName = pFile.split('\\')[-1]

    # read file
    dataFrame = pd.read_csv(pFile)

    # # convert to datetime
    dataFrame['DatetimeBegin'] = pd.to_datetime(dataFrame['DatetimeBegin'])

    # # calculate mask
    mask = dataFrame['DatetimeBegin'].between(year+'-04-01', year+'-04-30')

    # # output masked dataframes
    dataFrame[mask].to_csv(year+"_csv_april_filtered/"+fileName+"_filtered.csv", index=False)
    print("Done with filter "+fileName+", files left "+str( totalLenFiles-countFilesProccessed))
    countFilesProccessed += 1


#### Calculates the average per point

path = year+"_csv_april_filtered"
allFilteredFiles = glob.glob(os.path.join(path, "*.csv"))
totalLenFiles = len(allFilteredFiles)
countFilesProccessed = 1

for pFile in allFilteredFiles:
    # get file name
    fileName = pFile.split('\\')[-1]

    # read file
    dataFrame = pd.read_csv(pFile)

    # Calculate mask
    newDataFrame = dataFrame.groupby(['AirQualityStation', 'UnitOfMeasurement'])['Concentration'].agg(['mean']).reset_index()

    #calculate mean concentration
    newDataFrame.to_csv(year+"_csv_mean_concentration/"+fileName+"_mean_concentration.csv", index=False)
    print("saves mean concentration for "+fileName+", files left "+str( totalLenFiles-countFilesProccessed))
    countFilesProccessed += 1


#### concatenates all filtered files

path = year+"_csv_mean_concentration"
allFilteredFiles = glob.glob(os.path.join(path, "*.csv"))
totalLenFiles = len(allFilteredFiles)
countFilesProccessed = 1

for pFile in allFilteredFiles:
    dataFrame = pd.concat((pd.read_csv(f) for f in allFilteredFiles))
    print("Concatenates "+pFile.split('\\')[-1]+", files left "+str( totalLenFiles-countFilesProccessed))
    countFilesProccessed += 1

dataFrame.to_csv(year+"_csv_final_file_filtered/csv_filtered.csv", index=False)