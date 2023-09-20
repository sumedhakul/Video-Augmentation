import pandas as pd
import re
import json
import csv
import numpy as np
file_name='resources/subtitle/DJI_20230124113730_0001_W_Waypoint1.SRT'

frame_integer_re= '^[1-9]+$' #to check 1-9 and more than 9
df=pd.DataFrame(columns=['Time_Code','Frame_Number','Lattitude','Longtitude','Altitude','difftime'])

with open(file_name) as f:
    while line :=f.readline():
        lines= [line.rstrip('\n') for line in f]
        for index in range(len(lines)):
                line_str=lines[index]
                if re.search(frame_integer_re,line_str) !=None:
                        sequence_number=line_str
                        #print(sequence_number)

                        difftime_line=lines[index + 2]
                        difftime = float(difftime_line.split(': ')[2].split('ms')[0])
                        #print(difftime)

                        start_end_time=lines[index + 1]
                        start_time=start_end_time.split('-->')[0]
                        end_time=start_end_time.split('-->')[1]
                        #print(start_time)
                        #print(end_time)

                        time_c=lines[index + 3]
                        #print(time_code)
                        time_code=time_c.split(' ')[1]
                        #print(time_code)
                        frame=lines[index + 2]
                        frame_num=frame.split(',')[0][25:31]
                        #print(frame_num)
                        lat_long_alt=lines[index + 5]
                        lat=lat_long_alt.split('][')[0][10:19]
                        #print(lat)
                        long=lat_long_alt.split('][')[0][33:42]
                        #print(long)
                        alt=lat_long_alt.split('][')[0][54:62]
                        #print(alt)
        

                        entry = {
                            'Time_Code': time_code,
                            'Frame_Number': frame_num,
                            'Lattitude': lat,
                            'Longtitude': long,
                            'Altitude':alt,
                            'difftime':difftime
                        }
                        df.loc[len(df)]=entry
                        #index +=2



df['Distance'] = ''
df['Speed'] = ''
#print(df)


df['Lattitude'] = df['Lattitude'].astype('float64')
df['Longtitude'] = df['Longtitude'].astype('float64')
df['difftime'] = df['Longtitude'].astype('float64')

df.info()
#Start point coordinates
start_lat = 9.365171
start_lon = 80.089042

def haversine(lat1, lon1, lat2, lon2):
    # radius of the earth in km
    R = 6371  
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

#Distance   
df['Distance'] = df.apply(lambda row: haversine(start_lat, start_lon, row['Lattitude'], row['Longtitude']), axis=1)
print(df)

#calculate Speed 
def speed_calc(df, timecode, distance):
    time = df[timecode] / (1000 * 3600)

    # calculate the distance difference between rows in kilometers
    distance = df[distance]
    distance_diff = distance.diff() 

    # calculate the speed in kilometers per hour
    speed = distance_diff / time

    # add the new column to the original DataFrame
    df['Speed'] = speed

    return df

speed_calc(df,'difftime','Distance')

#Dataframe
df.drop('difftime', inplace=True, axis=1)
print(df)



# saving the dataframe
# Ask user to select format

print("Select a format to save the data:")
print("1. JSON")
print("2. CSV")
choice = int(input("Enter your choice (1 or 2): "))

# Save data in selected format
if choice == 1:
    df.to_json(r'resources\subtitle\dataframe.json')
    print("Data saved in JSON format.")
elif choice == 2:
    df.to_csv('resources\subtitle\DJI_20230124113730_0001_W_Waypoint1.csv')
    print("Data saved in CSV format.")
else:
    print("Invalid choice. Please enter 1 or 2.")


