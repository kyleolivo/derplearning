#!/usr/bin/env python3

import cv2
from datetime import datetime
import numpy as np
import os
import re
import sys
from time import strftime, gmtime, time

class Camera:
    
    def __init__(self, config, folder, has_model=False, index=None):
        """
        Open a camera capture
        """
        self.index = self.discoverCamera() if index is None else index
        self.config = config
        self.folder = folder
        self.mode = 'drive' if  has_model else 'record'

        self.width = self.config[self.mode]['width']
        self.height = self.config[self.mode]['height']
        self.fps = self.config[self.mode]['fps']

        # Input  video
        self.cap = cv2.VideoCapture(self.index)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        # Output video in log
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.extension = 'mp4'

        # Initialize known cameras
        path = os.path.join(self.folder, "camera_front.%s" % (self.extension))
        self.rec = cv2.VideoWriter(path, self.fourcc, self.fps, (self.width, self.height))

        
    def __del__(self):
        """
        Make sure we leave the camera for another program
        """
        self.cap.release()

        
    def getFrame(self):
        """
        Read the next camera frame. This is a blocking call
        """
        # Get time and steering angle
        ret, self.frame = self.cap.read()

        # If we can't get a frame don't return any and set a warning
        if not ret:
            sys.stderr.write("Failed to get frame!")
            return None
        return self.frame

    
    def record(self):
        self.rec.write(self.frame)

        
    def discoverCamera(self, last_available=True):  
        """
        Find available cameras, use most recently plugged in camera
        """
        devices = [int(f[-1]) for f in sorted(os.listdir('/dev')) if re.match(r'^video[0-9]', f)]
        if len(devices) == 0:
            return None
        device = devices[-1] if last_available else devices[0]
        return device
