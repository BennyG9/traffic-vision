from ultralytics import YOLO
import cv2
from pathlib import Path

VIDEO_PATH = "data/videos/video3.mp4"
OUTPUT_PATH = "outputs/video3_detected.mp4"
CONF = 0.25

def main():

    model = YOLO("yolo11n.pt")

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
    fourcc = cv2.VideoWriter.fourcc(*"mp4v")
    output_video = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

    if(not output_video.isOpened()):
        cap.release()
        raise RuntimeError("Could not create output video file")

    frame_index = 0

    print("Starting...")

    try:
        while(True):
            ret, frame = cap.read()

            if(not ret):
                break

            model_results = model(frame, device=0, conf=CONF, verbose=False)

            annotated_frame = model_results[0].plot()

            output_video.write(annotated_frame)

            frame_index += 1

    finally:
        cap.release()
        output_video.release()
        cv2.destroyAllWindows()
        print("Done!")

    pass


if __name__ == "__main__":
    main()