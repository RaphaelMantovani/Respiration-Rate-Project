from tkinter import N
import numpy as np
import cv2 as cv 
import matplotlib.pyplot as plt
import pandas as pd
from more_itertools import locate
import json, os
from scipy.signal import find_peaks

# set base path
base_path = "C:/Users/Raphael/OneDrive/Documentos/respiration_project/"

# get json data
with open(base_path + "respiration_rate_large_sample_json.json", 'r') as f:
    json_data = json.load(f)

# access index values
all_files = os.listdir(base_path + "sample_test/frames/")
cam_indexes = [int(a.split("CAM")[1]) for a in all_files]
all_files = sorted(all_files, key = lambda x: int(x.split("CAM")[1]))
first_index = int(all_files[0].split("CAM")[1])
last_index = int(all_files[-1].split("CAM")[1])

# create empty list to store dictionary with cow name, camera, predicted breaths
data_list = []

# define breath predicting function
def breath_predictor(video):
    global json_data, base_path, data_list
    
    for frame in json_data['frames']:
        if frame.split('.')[0] + '.mp4' == video:
            new_frame = frame
            break
    print(new_frame)

    for cow in json_data['frames'][new_frame]["regions"]:
        cap = cv.VideoCapture(base_path + "sample_test/30_sec_videos/CAM" + new_frame.split(' ')[0].split('AM')[1] + "/" + str(video))
        assert cap.isOpened(), "video can't be opened... is the path correct?"

        fps = cap.get(cv.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
        nframes = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        duration = nframes / fps

        roi_x = cow['shape_attributes']['x']
        roi_y = cow['shape_attributes']['y']
        roi_width = cow['shape_attributes']['width']
        roi_height = cow['shape_attributes']['height']
        cow_name = cow['region_attributes']['name']

        cube = np.empty((nframes, roi_height, roi_width, 3), dtype=np.uint8)
        # 3-channel: assuming it's RGB/BGR data, not gray

        for i in range(nframes):
            rv, frame1 = cap.read()
            assert rv, "video ended before it said it would!"
            cube[i] = frame1[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

        cap.release()

        #channel 1 only
        pixelRed = cube[:,:,:,0:1]
        pixelRed.shape

        pixelGreen = cube[:,:,:,1:2]
        pixelGreen.shape

        pixelBlue = cube[:,:,:,2:3]
        pixelBlue.shape

        #get average pixel red channel for ROI
        respRed = pd.DataFrame(pixelRed.reshape(nframes,roi_width*roi_height))
        respRed['mean_Red'] = respRed.mean(axis=1)
        respRed

        #get average pixel green channel for ROI
        respGreen = pd.DataFrame(pixelGreen.reshape(nframes,roi_width*roi_height))
        respGreen['mean_Green'] = respGreen.mean(axis=1)
        respGreen

        #get average pixel blue channel for ROI
        respBlue = pd.DataFrame(pixelBlue.reshape(nframes,roi_width*roi_height))
        respBlue['mean_Blue'] = respBlue.mean(axis=1)
        respBlue

        b = respBlue['mean_Blue']
        g = respGreen['mean_Green']
        r = respRed['mean_Red']
        frames = [b, g, r]
        frames

        ########## Applying Fourier Transform ###########
        step = 1 / fps
        t = np.arange(0, duration, step)
        n = len(t)
        xhat = np.fft.fft(b, n)
        # print(xhat)
        PSD = xhat * np.conj(xhat) / n
        freq = (duration /(step*n)) * np.arange(n)
        L = np.arange(1, np.floor(n/2), dtype='int')
    
        freq_cond = []
        for frequency in freq:
            condition = 10 < frequency < 50
            freq_cond.append(condition)

        PSDclean = [a.real for a in PSD] * np.array(freq_cond)
        PSD_np = np.array(PSDclean[L])
        ind = np.argpartition(PSD_np, -5)[-5:].tolist()
        # top4_PSD = PSD_np[ind].tolist()

        # get list with 1 for the top 5 PSD values and 0 for the rest
        indexes = list(locate(xhat))
        index = 0
        while index < len(indexes):
            if indexes[index] in ind:
                indexes[index] = 1
            else:
                indexes[index] = 0
            index += 1

        xhat = indexes * xhat
        # print(xhat)
        xfilt = np.fft.ifft(xhat)
        # print(xfilt)
        ####### Finding peaks in filtered data ##########
        xpeaks, _ = find_peaks(xfilt)
        predicted_breaths = len(xpeaks)
        print(predicted_breaths)

        ###### Append data to list #######
        if '(2)' in video:
            vid_number = 2
        else:
            vid_number = 1
        dict_data = {'CAM': int(video.split('h')[0].split(' ')[0].split('CAM')[1]), 
        'cow_number': int(cow_name.split('ow')[1]), 
        'day' : int(video.split('h')[0].split(' ')[1]),
        'hour' : int(video.split('h')[0].split(' ')[2]), 
        'vid_number' : vid_number,
        'predicted_breaths': predicted_breaths}

        data_list.append(dict_data)

# use function for every video in directory
for var in range(first_index, last_index + 1):
    if var in cam_indexes:
        for data in os.listdir(base_path + "sample_test/30_sec_videos/CAM" + str(var)):
            breath_predictor(data)

# save data to csv file
rr_data = pd.DataFrame.from_dict(data_list)

os.chdir(base_path + 'excel/')
rr_data.to_excel('full_sample_test_freq5.xlsx')