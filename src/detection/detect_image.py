def detect_image(image_path, model, conf, show=False):

    #get model outputs 
    model_results = model(image_path, device=0, conf=conf, verbose=False, rect=False, imgsz=416)

    #package important information
    results = {
        "raw": model_results[0],
        "boxes": [
            {
                "class_id": int(box.cls[0]),
                "confidence": float(box.conf[0]),
                "coordinates": box.xyxy[0].tolist(),
                "class_name": model_results[0].names[int(box.cls[0])]
            }
            for box in model_results[0].boxes
        ],
        "annotated_image": model_results[0].plot()        
    }

    if(show):
        model_results[0].show()

    return results 



if __name__ == "__main__":
    pass
