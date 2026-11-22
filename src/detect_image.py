#The purpose of this script is to learn how to use YOLO

from ultralytics import YOLO
import cv2

#load pretrained yolo nano model
model = YOLO("yolo11n.pt")

#run model on test image
results = model("data/images/test.jpg", device=0, conf=0.25)

#disp results
result = results[0]

#print(result.boxes)

print("\nDetected objects:")
for box in result.boxes:
    class_id = int(box.cls[0])
    confidence = float(box.conf[0])
    coordinates = box.xyxy[0].tolist()
    class_name = result.names[class_id]

    print(
        f"Class: {class_name:15s} "
        f"Confidence: {confidence:.3f} "
        f"Bounding box: {coordinates}"
    )

#annotated image
result.show()