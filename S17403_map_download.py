import pandas as pd
import requests

csv_file='resources/subtitle/DJI_20230124113730_0001_W_Waypoint1.csv'
map_dir='resources/map'

def download_image(image_url,path_to_write):
    img_data=requests.get(image_url).content

    with open(path_to_write,'wb') as handler:
        handler.write(img_data)

df=pd.read_csv(csv_file)

for index, row in df.iterrows():
    #print(str(index), row['lat'],row['lng'])

    url ="https://maps.googleapis.com/maps/api/staticmap?center={0},{1}&zoom=13&size=400x300&maptype=hybrid&markers=color:red%7Clabel:S%7C{0},{1}&markers=size:tiny%22&key=AIzaSyCUIK90jYIXusR43siewRD9Rw2gtPI-7lg&path=color:0x0000ff|weight:3".format(row["Lattitude"],row["Longtitude"])
    download_image(url,map_dir + "/" + str(index) + ".png")
    print(str(index),"downloaded")


