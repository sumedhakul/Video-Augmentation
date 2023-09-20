import cv2 as cv
import numpy as np
from os.path import exists
import pandas as pd
from moviepy.video.io.VideoFileClip import VideoFileClip



# # Load the video file
# video = VideoFileClip("resources/subtitle/DJI_20230124113730_0001_W_Waypoint1.mp4")

# # Extract the first 20 seconds
# subclip = video.subclip(0, 20)

# # Save the subclip as a new file
# subclip.write_videofile("resources/subtitle/DJI_20230124113730_0001_W_Waypoint1_output_video.mp4", fps=video.fps)

file_prefix='resources/subtitle/DJI_20230124113730_0001_W_Waypoint1'
waypoint_srt_records=pd.read_csv(file_prefix + '.csv')

window_name='Processing'
file_name=file_prefix + "_output_video.mp4"

#video = cv.VideoCapture(file_prefix + "_output_video.mp4")
cv.namedWindow(window_name,cv.WINDOW_NORMAL)

source=cv.VideoCapture(file_name)
framepersecond=float(source.get(cv.CAP_PROP_FPS))
success,image=source.read()
height, width, layers=image.shape
out=cv.VideoWriter(file_prefix + "_processed.mp4", cv.VideoWriter_fourcc(*"mp4v"),framepersecond,(width,height))
video_frame_count=1
alpha=0.7


for index, row in waypoint_srt_records.iterrows():
    Speed = str(row['Speed']) 
    Lattitude = str(row['Lattitude'])  
    Longtitude = str(row['Longtitude'])
    Frame_Number = row['Frame_Number'] 
    


# Extract the speed and latitude columns
Speed = waypoint_srt_records['Speed']
Lattitude = waypoint_srt_records['Lattitude']

while success and (cv.waitKey(1) & 0xFF !=ord('q')):#27 for ESC

    frame_index=int(video_frame_count/framepersecond)
    map_file='resources/map/' + str(frame_index) + '.png'

    overlay=image.copy()

    #speed,lat,lng,distance from the strating- point
    #cv.line(overlay,(100,100),(1000,100),(50,50,50),100)
    cv.line(overlay,(900,1000),(1750,1000),(50,50,50),120)
    cv.putText(overlay,"SPEED(km/h)",(900,1000),cv.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2,1)
    cv.putText(overlay,"Lat",(1380,1000),cv.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2,1)
    cv.putText(overlay,"Long",(1575,1000),cv.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2,1)
    cv.putText(overlay,"Alt",(1380,1040),cv.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2,1)

    speed = waypoint_srt_records.loc[frame_index,'Speed']
    cv.putText(overlay, str(speed), (1095, 1000), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, 1)   

    Lattitude = waypoint_srt_records.loc[frame_index,'Lattitude']
    cv.putText(overlay, str(Lattitude), (1430, 1000), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, 1)

    Longtitude = waypoint_srt_records.loc[frame_index,'Longtitude']
    cv.putText(overlay, str(Longtitude), (1650, 1000), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, 1) 
   
    Altitude = waypoint_srt_records.loc[frame_index,'Altitude']
    cv.putText(overlay, str(Altitude), (1430, 1040), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, 1)
    
    
    
    video_frame_count+=1
    
    
    result=cv.addWeighted(overlay, alpha, image, 1 - alpha,0)

    if exists(map_file):
        map=cv.imread(map_file, -1)
        result[770:1070,10:410]=map[0:300,0:400]

    out.write(result)
    cv.imshow(window_name,result)
    success,image=source.read()

    if video_frame_count % 30 ==0:
        print("working")
    
    
    video_frame_count+=1
    
    
source.release()
out.release()
cv.destroyAllWindows()
print('completed')