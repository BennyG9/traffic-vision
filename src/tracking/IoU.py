#box = {class_id, confidence, coordinates, class_name}
def IoU(box1, box2):

    x_left = max(box1["coordinates"][0], box2["coordinates"][0])
    x_right = min(box1["coordinates"][2], box2["coordinates"][2])
    y_top = min(box1["coordinates"][1], box2["coordinates"][1])
    y_bottom = max(box1["coordinates"][3], box2["coordinates"][3])

    width = max(0, x_right - x_left)
    height = max(0, y_bottom - y_top)

    intersection = width * height

    area1 = (box1["coordinates"][2] - box1["coordinates"][0]) * (box1["coordinates"][3] - box1["coordinates"][1])
    area2 = (box2["coordinates"][2] - box2["coordinates"][0]) * (box2["coordinates"][3] - box2["coordinates"][1])
    union = area1 + area2 - intersection

    return abs(intersection / union) if union > 0 else 0.0