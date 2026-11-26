import cv2

def annotate_tracks(frame, tracks):
    for track in tracks:
        #box coordinates
        x1, y1, x2, y2 = map(int, track.coordinates)

        #draw bounding box
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

        #draw label
        label = f"{track.class_name} | ID: {track.track_id}"
        cv2.putText(frame, label, (x1,y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2)

    return frame