from ultralytics import YOLO
import cv2
from pathlib import Path

VIDEO_PATH = "/data/videos/video3.mp4"
OUTPUT_PATH = "outpus/video3_detected.mp4"
CONF = 0.25

def main():

    model = YOLO("yolo11n.pt", device=0, conf=CONF)

    #open video
    cap = cv2.VideoCapture(VIDEO_PATH)

    #check if successfuly opened
    if(not cap.isOpened()):
        raise RuntimeError("Could not open video")

    #video properties 
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    #prepare script output
    Path("outputs").mkdir(exist_ok=True)


    




    pass