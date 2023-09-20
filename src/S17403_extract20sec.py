from moviepy.video.io.VideoFileClip import VideoFileClip

# Load the video file
video = VideoFileClip("resources/subtitle/DJI_20230124113730_0001_W_Waypoint1.mp4")

# Extract the first 20 seconds
subclip = video.subclip(0, 20)

# Save the subclip as a new file
subclip.write_videofile("resources/subtitle/DJI_20230124113730_0001_W_Waypoint1_output_video.mp4", fps=video.fps)