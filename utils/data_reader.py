from threading import Thread
import time
from typing import List
import os

import cv2


class DataReader:
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
