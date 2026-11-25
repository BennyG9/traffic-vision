import cv2
from pathlib import Path
import torch
import time 
import numpy as np

def run_benchmarks(video_path, model, conf, warmup=10, disp=False):

    #open video
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    #check if successfuly opened
    if(not cap.isOpened()):
        raise RuntimeError("Could not open video")

    frame_index = 0

    frame_proc_duration = np.zeros(frame_count)
    global_elapsed = 0

    print("Starting...")

    try:
        while(True):
            ret, frame = cap.read()

            if(not ret):
                break

            torch.cuda.synchronize()
            start = time.perf_counter()
 
            model_results = model(frame, device=0, conf=conf, verbose=False)

            torch.cuda.synchronize()
            elapsed = time.perf_counter() - start
            if(frame_index == warmup-1): global_elapsed = time.perf_counter()
            frame_proc_duration[frame_index] = elapsed

            frame_index += 1

    finally:
        global_elapsed = time.perf_counter() - global_elapsed
        cap.release()


    frame_proc_duration = frame_proc_duration[10:]

    #calculate benchmarks 
    duration_mean = np.mean(frame_proc_duration)
    duration_median = np.median(frame_proc_duration)
    duration_std = np.std(frame_proc_duration)
    duration_95pct = np.percentile(frame_proc_duration, 95)
    duration_min = np.min(frame_proc_duration)
    duration_max = np.max(frame_proc_duration)
    mean_fps = 1 / duration_mean

    if(disp):
        print("----- Benchmarks -----")
        print(f"Frames:\t\t{frame_count:.0f}")
        print(f"Total Time:\t{global_elapsed:.5f}")
        print(f"Mean:\t\t{duration_mean:.5f}")
        print(f"Median:\t\t{duration_median:.5f}")
        print(f"STD:\t\t{duration_std:.5f}")
        print(f"95 PCT:\t\t{duration_95pct:.5f}")
        print(f"Min:\t\t{duration_min:.5f}")
        print(f"Max:\t\t{duration_max:.5f}")
        print(f"FPS:\t\t{mean_fps:.5f}")

    benchmarks = {
        "frames": frame_count,
        "total_time": global_elapsed,
        "mean": duration_mean,
        "median": duration_median,
        "std": duration_std,
        "pct95": duration_95pct,
        "min": duration_min,
        "max": duration_max,
        "fps": mean_fps
    }
    return benchmarks


if __name__ == "__main__":
    pass