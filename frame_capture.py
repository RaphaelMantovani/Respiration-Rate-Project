import cv2 as cv
import os
from glob import glob

base_path = "C:/Users/Raphael/OneDrive/Documentos/respiration_project/sample_test/"
origin_path = base_path + "30_sec_videos/CAM" 
destination_path = base_path + "frames/CAM"

all_files = os.listdir(base_path + "frames/")
cam_indexes = [int(a.split("CAM")[1]) for a in all_files]
all_files = sorted(all_files, key = lambda x: int(x.split("CAM")[1]))
first_index = int(all_files[0].split("CAM")[1])
last_index = int(all_files[-1].split("CAM")[1])

for index in range(first_index, last_index + 1):
    if index in cam_indexes:
        os.chdir(destination_path + str(index))
        for video in os.listdir(origin_path + str(index)):
            vidcap = cv.VideoCapture(origin_path + str(index) + "/" + str(video))
            ret,frame = vidcap.read()
            print(video)
            if ret:
                cv.imwrite(destination_path + str(index) + "/" + str(video).replace('.mp4', '.jpeg'), frame)
            vidcap.release()
            cv.destroyAllWindows()