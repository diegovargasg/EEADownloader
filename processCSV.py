import pandas as pd
import os
import glob
import psycopg2

from dotenv import load_dotenv

load_dotenv()
YEAR=os.getenv('YEAR')
DBHOST=os.getenv('DBHOST') 
DBNAME=os.getenv('DBNAME')
DBUSER=os.getenv('DBUSER')
DBPASS=os.getenv('DBPASS')

##### Clean up all folders

dir = YEAR+"_csv_april_filtered"
filelist = glob.glob(os.path.join(dir, "*"))
for f in filelist:
    os.remove(f)

### Filters the date by april

path = YEAR+"_csv"
allFiles = glob.glob(os.path.join(path, "*.csv"))
totalLenFiles = len(allFiles)
countFilesProccessed = 1

for pFile in allFiles:
    fileName = pFile.split('\\')[-1]
    fileName = fileName.split('.')[0]

    # read file and ignore invalid entries
    dataFrame = pd.read_csv(pFile, usecols = ['AirQualityStation','Concentration', 'DatetimeBegin', 'Validity'])
    dataFrame = dataFrame[(dataFrame["Validity"] == 1)]

    # convert to datetime
    dataFrame['DatetimeBegin'] = pd.to_datetime(dataFrame['DatetimeBegin'])

    # calculate mask
    mask = dataFrame['DatetimeBegin'].between(YEAR+'-04-01', YEAR+'-04-30')

    ## output masked dataframes
    dataFrame[mask].to_csv(YEAR+"_csv_april_filtered/"+fileName+".csv", index=False)
    print("Done with filter "+fileName+", files left "+str( totalLenFiles-countFilesProccessed))
    countFilesProccessed += 1

#### Stores the filtered CSV in the database

conn = psycopg2.connect("host="+DBHOST+" dbname="+DBNAME+" user="+DBUSER+" password="+DBPASS+"")
cur = conn.cursor()

path = YEAR+"_csv"
allFiles = glob.glob(os.path.join(path+"_april_filtered/", "*.csv"))
totalLenFiles = len(allFiles)
countFilesProccessed = 1

cur.execute("DROP TABLE IF EXISTS year_"+YEAR+";")

cur.execute('''CREATE TABLE year_'''+YEAR+'''(
  AirQualityStation        VARCHAR(100) NOT NULL,
  Concentration            DECIMAL NOT NULL,
  DatetimeBegin            VARCHAR(100) NOT NULL,
  Validity                 INTEGER  NOT NULL
);''')

for pFile in allFiles:
    fileName = pFile.split('\\')[-1]

    # read file
    dataFrame = pd.read_csv(pFile)

    with open('D:/Projekte/basic_server/'+path+"_april_filtered/"+fileName, 'r') as f:
  
        next(f) #  To Skip the header row.
        cur.copy_from(f, 'year_'+YEAR, sep=',')

    conn.commit()
    
    print("Save in Database "+fileName+", files left "+str( totalLenFiles-countFilesProccessed))
    countFilesProccessed += 1