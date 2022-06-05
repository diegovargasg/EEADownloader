# importing csv module
import pandas as pd
import os
import glob
 
# path = "csv"
# all_files = glob.glob(os.path.join(path, "*.csv"))

# for pFile in all_files:
#     fileName = pFile.split('\\')[-1]
#     print("Ready to filter "+fileName)

#     # read file
#     df = pd.read_csv(pFile)

#     # # convert to datetime
#     df['DatetimeBegin'] = pd.to_datetime(df['DatetimeBegin'])

#     # # calculate mask
#     mask = df['DatetimeBegin'].between('2020-04-01', '2020-04-30')

#     # # output masked dataframes
#     df[mask].to_csv("csv_filtered/"+fileName+"_filtered.csv", index=False)
#     print("Done with filter "+fileName)

# concatenates all filtered files

path = "csv_filtered"
all_filtered_files = glob.glob(os.path.join(path, "*.csv"))

li = []

for pFile in all_filtered_files:
    print("Concatenates "+pFile.split('\\')[-1])
    df = pd.concat((pd.read_csv(f) for f in all_filtered_files))
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
frame.to_csv("csv_single_file_filtered/csv_filtered.csv", index=False)