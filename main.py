from typing import List
from threading import Thread
import time
import os

import cv2
import numpy as np
import pandas as pd


class FrameReader:
    def __init__(self, directory: str):
        # get all the frames from a video
        self._frames = []
        self._cap = cv2.VideoCapture(os.path.join(directory, "output.avi"))
        self._read_thread = Thread(target=self._read_frames).start()

        # TODO load the imu data
        pass

        # wait until one frame has appeared
        while len(self._frames) == 0:
            time.sleep(0.0001)

    @property
    def frames(self) -> List:
        return self._frames

    def _read_frames(self):
        while True:
            got_frame, frame = self._cap.read()
            if not got_frame:
                break
            self._frames.append(frame)

def main():
    # stuff
    # calibrate me
    K = np.array([
        [3060.68701171875, 0.0, 1997.737548828125],
        [0.0, 3060.68701171875, 860.2412109375],
        [0.0, 0.0, 1.0]
    ])
    markerLength = 0.08  # meters

    # read video
    reader = FrameReader("data/1667355041/")
    
    for frame in reader.frames:
    # detect marker!!!
        aDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
        corners, ids, _ = cv2.aruco.detectMarkers(frame, aDict)
        cv2.aruco.drawDetectedMarkers(frame, corners, ids, borderColor=(0,0,255))
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, markerLength, K, None)

        

        cv2.imshow("hello", frame)
        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == "__main__":
    main()
