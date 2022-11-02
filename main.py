from typing import List
from threading import Thread
import cv2
import numpy as np

from utils.data_reader import DataReader


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
    reader = DataReader("data/1667355041/")
    
    for frame in reader.frames:
    # detect marker!!!
        aDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
        corners, ids, _ = cv2.aruco.detectMarkers(frame, aDict)
        cv2.aruco.drawDetectedMarkers(frame, corners, ids, borderColor=(0,0,255))
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, markerLength, K, None)

        if rvecs is None or tvecs is None:
            cv2.imshow("window", frame)
            if cv2.waitKey(1) == ord('q'):
                break
            continue

        # only care about 1 marker
        rvec = rvecs[0]
        tvec = tvecs[0]

        cv2.drawFrameAxes(frame, K, None, rvec, tvec, markerLength)

        # make a transform
        

        cv2.imshow("window", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
