from ultralytics import YOLO
import cv2
from detection.detect_image import detect_image
from detection.detect_video import detect_video
from evaluation.run_benchmarks import run_benchmarks
import time

TEST_IMAGE = "data/images/test.jpg"

TEST_VIDEO = "data/videos/video6.mp4"
OUTPUT_FILE = "outputs/video6_detected.mp4"

CONFIDENCE = 0.25
MODEL = YOLO("yolo11n.pt")

#TEST IMAGE DETECTION
#results = detect_image(image_path=TEST_IMAGE, model=MODEL, conf=CONFIDENCE, show=True)
#print(results.keys())


#TEST VIDEO DETECTION
# last_frame_time = time.perf_counter()
# for results, metadata in detect_video(video_path=TEST_VIDEO, model=MODEL, conf=CONFIDENCE, output_path=OUTPUT_FILE):

#     current_time = time.perf_counter()
#     elapsed = current_time = last_frame_time
    
#     frame = results["annotated_image"]
#     cv2.imshow("RoadVision", frame)

#     remaining = max((1 / metadata["fps"]) - elapsed, 0.001)
#     remaining_ms = int(remaining * 1000)

#     if cv2.waitKey(remaining_ms) & 0xFF == ord("q"):
#         break

#     last_frame_time = time.perf_counter()
# cv2.destroyAllWindows()


#TEST VIDEO BENCHMARKING
benchmarks = run_benchmarks(TEST_VIDEO, MODEL, CONFIDENCE, disp=True)