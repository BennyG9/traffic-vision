import cv2
from pathlib import Path
from .detect_image import detect_image

def detect_video(video_path, model, conf, output_path=None):

    #open video
    cap = cv2.VideoCapture(video_path)
    if(not cap.isOpened()):
        raise RuntimeError("Could not open input video")

    #video properties 
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_metadata = {
        "fps": fps,
        "width": width,
        "height": height,
        "frame_count": frame_count,
    }

    #frame_index = 0

    #prepare output file when called for
    output_file = None
    if(output_path is not None):
        Path("outputs").mkdir(exist_ok=True)
        fourcc = cv2.VideoWriter.fourcc(*"mp4v")
        output_file = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        if(not output_file.isOpened()):
            cap.release()
            raise RuntimeError("Unable to create output file")

    try:
        while(True):
            #pull data frame by frame
            ret, frame = cap.read()
            if(not ret):
                break

            #get model outputs
            results = detect_image(frame, model, conf)

            #function output
            if(output_file is not None):
                output_file.write(results["annotated_image"])
            yield results, video_metadata 
            

            #frame_index += 1

    finally:
        cap.release()
        if(output_file is not None): 
            output_file.release()
    pass




if __name__ == "__main__":
    pass