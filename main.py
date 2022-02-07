import cv2
import numpy as np
import os, os.path
import time
from datetime import datetime
import pyrebase
import json

with open('camera.json', 'r') as f:
    camera = json.load(f)

config = {
  "apiKey": "AIzaSyBTdUpEpEcx-eie9LFU43B-DwTG9KImXXE",
  "authDomain": "hides-4821e.firebaseapp.com",
  "databaseURL": "https://hides-4821e-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "hides-4821e",
  "storageBucket": "hides-4821e.appspot.com",
  "messagingSenderId": "873480647084",
  "appId": "1:873480647084:web:8fd2d67591226a9a340a09",
  "measurementId": "G-F7S16RQPKC",
  "serviceAccount": "serviceAccount.json"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()
storage = firebase.storage()

capture_list = database.child("Capture").shallow().get().val()

if capture_list is not None:
    capture_count = len(capture_list)

else:
    capture_count = 0

import jetson.utils
camera = jetson.utils.gstCamera(1280, 720, "0")
#display =  jetson.utils.glDisplay()

import jetson.inference
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

last_detect_time = 0
current_time =time.time()

def save_video(frame, width, height, writer):
	conversion1 = jetson.utils.cudaToNumpy(frame, width, height, 4)        
	conversion2 = cv2.cvtColor(conversion1, cv2.COLOR_RGBA2RGB).astype(np.uint8)
	conversion3 = cv2.cvtColor(conversion2, cv2.COLOR_RGB2BGR)
	writer.write(conversion3)

while True:
	current_time = time.time()
	img, width, height = camera.CaptureRGBA(zeroCopy = 1)
	detections = net.Detect(img, width, height)

	#saving video if detect person
	if(len(detections) > 0):
		detected_object = detections[0].ClassID
		if detected_object == 1:	
			if current_time - last_detect_time > 5:
				fourcc = cv2.VideoWriter_fourcc(*'avc1')
				writerX = cv2.VideoWriter('Capture/' + datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + '.mp4', fourcc, 20.0, (width, height))
				save_video(img, width, height, writerX)
			
			else:
				save_video(img, width, height, writerX)
		
			last_detect_time = current_time
		else:
			if current_time - last_detect_time < 5:
				save_video(img, width, height, writerX)
			else:
				if 'writerX' in locals():
					writerX.release()
					
	else:
		if current_time - last_detect_time < 5:
			save_video(img, width, height, writerX)
		
		else:
			if 'writerX' in locals():
				writerX.release()
				
	
		
	
