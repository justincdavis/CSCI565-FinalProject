import os
import time

import cv2
import depthai as dai


class Camera:
    def __init__(self):
        # Create pipeline
        self.pipeline = dai.Pipeline()

        # Define source and output
        self.camRgb = self.pipeline.create(dai.node.ColorCamera)
        self.xoutVideo = self.pipeline.create(dai.node.XLinkOut)

        self.xoutVideo.setStreamName("video")

        # Properties
        self.camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        self.camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        self.camRgb.setVideoSize(1920, 1080)

        self.xoutVideo.input.setBlocking(False)
        self.xoutVideo.input.setQueueSize(1)

        # Linking
        self.camRgb.video.link(self.xoutVideo.input)

        # OpenCV VideoWriter
        # create the directory for this data
        self.data_dir = os.path.join(os.getcwd(), f"data/{int(time.time())}")
        os.mkdir(self.data_dir)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.writer = cv2.VideoWriter(os.path.join(self.data_dir, 'output.avi'), fourcc, 30.0, (1920, 1080))

        # TODO setup IMU
        pass


    def record(self):
        # Connect to device and start pipeline
        with dai.Device(self.pipeline) as device:

            video = device.getOutputQueue(name="video", maxSize=1, blocking=False)

            while True:
                videoIn = video.get()
                frame = videoIn.getCvFrame()

                # write frame
                self.writer.write(frame)

                # Get BGR frame from NV12 encoded video frame to show with opencv
                # Visualizing the frame on slower hosts might have overhead
                cv2.imshow("video", frame)

                if cv2.waitKey(1) == ord('q'):
                    break

        self.writer.release()
    

if __name__ == "__main__":
    cam = Camera()
    cam.record()
