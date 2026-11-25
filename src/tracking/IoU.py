#box = {class_id, confidence, coordinates, class_name}
def IoU(xyxy1, xyxy2):

    x_left = max(xyxy1[0], xyxy2[0])
    x_right = min(xyxy1[2], xyxy2[2])
    y_top = min(xyxy1[1], xyxy2[1])
    y_bottom = max(xyxy1[3], xyxy2[3])

    width = max(0, x_right - x_left)
    height = max(0, y_bottom - y_top)

    intersection = width * height

    area1 = (xyxy1[2] - xyxy1[0]) * (xyxy1[3] - xyxy1[1])
    area2 = (xyxy2[2] - xyxy2[0]) * (xyxy2[3] - xyxy2[1])
    union = area1 + area2 - intersection

    return (intersection / union) if union > 0 else 0.0