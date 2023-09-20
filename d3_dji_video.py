import cv2 as cv
import numpy as np
import csv
from os.path import exists

def read_csv(geo_json_csv):

    video_second_record = list()

    with open(geo_json_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        pre_distance = 0
        path_tracker = list()
        meters_per_second_to_kmh = 0.0333 / 3.6
        
        for row in csv_reader:
            if line_count != 0:
                cur_distance = float(row["DISTANCE"])
                speed = (cur_distance - pre_distance) / meters_per_second_to_kmh
                video_second_record.append({"frame_no":line_count, "speed": speed, "lat":row["LATITUDE"], "lon": row["LONGITUDE"]})
                #print(f'\t{row["TIMECODE"]} Lat {row["LATITUDE"]} Lng {row["LONGITUDE"]} Distance {row["DISTANCE"]} Speed {round(speed, 2)}')
                pre_distance = cur_distance
            
            line_count += 1

    return video_second_record

file_prefix = "202301241132_006_Veravil/Set1/DJI_20230124113730_0001_S_Waypoint1"
waypoint_srt_records = read_csv(file_prefix+'.csv')

window_name = 'Veravil'
file_name = file_prefix + ".MP4"
cv.namedWindow(window_name, cv.WINDOW_NORMAL)

source = cv.VideoCapture(file_name)   
success, image = source.read()
factor = 2
height, width, layers = image.shape

new_h = height // factor
new_w = width // factor

framespersecond= float(source.get(cv.CAP_PROP_FPS))

x, y, w, h = 100, 100, 200, 100
sub_img = image[y:y+h, x:x+w]

line_start = (1000, 950)
line_end = (1600, 950)
line_color = (50,50,50)
line_tickness = 100
alpha = 0.7

font = cv.FONT_HERSHEY_COMPLEX
bottomLeftCornerOfText = (1000,500)
fontScale  = 0.8
fontScale_var = 1.4
fontColor = (255, 255, 255)
thickness = 2
lineType = 1

video_frame_count = 1

cv.putText(image,'Speed', bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
out = cv.VideoWriter(file_prefix + "_processed.mp4", cv.VideoWriter_fourcc(*'MP4V'), framespersecond, (width, height))

speed_print = ''
lat_print = ''
lon_print = ''

map = cv.imread(file_prefix + "/1.png", -1)
total_frames = int(source.get(cv.CAP_PROP_FRAME_COUNT))
while success and (cv.waitKey(1) & 0xFF != ord('q')):  # 27 for esc

    frame_index = int(video_frame_count / framespersecond)
    #print(frame_index)
    image_index = int(frame_index / 30)
    #print(file_prefix + "/" + str(frame_index) + ".png")
    if frame_index == 0:
        frame_index = 1

    map_file_name = file_prefix + "/" + str(frame_index) + ".png"

    if exists(map_file_name):
        map = cv.imread(file_prefix + "/" + str(frame_index) + ".png", -1)
    
    if len(waypoint_srt_records) > frame_index:
        frame_info = waypoint_srt_records[frame_index]
        #speed_print = frame_info['speed']
        lat_print = frame_info['lat']
        lon_print = frame_info['lon']

        speed_print = str(sum(d['speed'] for d in waypoint_srt_records[video_frame_count: video_frame_count+30]) / 30)
        
    overlay = image.copy()

    cv.line(overlay, line_start, line_end, line_color, line_tickness)
    cv.putText(overlay, 'SPEED (km/h)', (line_start[0] - 10, line_start[1] + 30), font, fontScale, fontColor, thickness, lineType)
    cv.putText(overlay, str(speed_print)[:5], (line_start[0] - 10, line_start[1] - 10), font, fontScale_var, fontColor, thickness, lineType)
    
    cv.putText(overlay, '100', (line_start[0] + 220, line_start[1] - 10), font, fontScale_var, fontColor, thickness, lineType)
    cv.putText(overlay, 'ALTITUDE (m)', (line_start[0] + 200, line_start[1] + 30), font, fontScale, fontColor, thickness, lineType)
    
    cv.putText(overlay, 'LON:', (line_start[0] + 400, line_start[1] - 10), font, fontScale, fontColor, thickness, lineType)
    cv.putText(overlay, str(lon_print), (line_start[0] + 480, line_start[1] - 10), font, fontScale, fontColor, thickness, lineType)
    cv.putText(overlay, 'LAT:', (line_start[0] + 400, line_start[1] + 30), font, fontScale, fontColor, thickness, lineType)
    cv.putText(overlay, str(lat_print), (line_start[0] + 480, line_start[1] + 30), font, fontScale, fontColor, thickness, lineType)

    result = cv.addWeighted(overlay, alpha, image, 1 - alpha, 0)
    #map_result = cv.addWeighted(map_overlay, 0.4, image, 0.5, 0)

    result[790:1070 , 10:410] = map[0:280, 0:400]
    
    out.write(result)
    resize = cv.resize(result, (new_w, new_h), interpolation=cv.INTER_AREA)
    cv.imshow(window_name, resize)
    video_frame_count += 1

    success, image = source.read()

source.release()
out.release()
cv.destroyAllWindows()

