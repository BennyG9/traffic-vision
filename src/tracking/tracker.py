from .association import association
from .track import Track
import cv2

class Tracker():

    def __init__(self):
        self.tracks = []
        self.next_track_id = 0
        pass


    def update(self, detections):

        #object and track associations 
        matches, unmatched_tracks, unmatched_objects = association(self.tracks, detections, 0.3)

        #update tracks with matched objects
        for indices in matches:
            box = detections["boxes"][indices["object_index"]]
            self.tracks[indices["track_index"]].log_hit(box["coordinates"], box["confidence"])
            pass

        #udpate tracks without matched objects
        for track_index in unmatched_tracks:
            self.tracks[track_index].log_miss()
            pass

        #create new tracks for all unmatched objects
        for object_index in unmatched_objects:
            box = detections["boxes"][object_index]
            new_track = Track(self.next_track_id, box["class_id"], box["class_name"], box["coordinates"], box["confidence"])
            self.tracks.append(new_track)
            self.next_track_id += 1
            pass

        #remove outdated tracks
        self.tracks = [track for track in self.tracks if(track.missed_frames < track.MAX_MISSED)]

        #return active tracks 
        return self.tracks

    pass



class Counter():

    def __init__(self, endpt1, endpt2):
        self.line = {
            "endpt1": endpt1,
            "endpt2": endpt2,

            "delta_x": endpt2[0] - endpt1[0],
            "delta_y": endpt2[1] - endpt1[1],
        }
        self.counter = 0
        self.tracks = {}
        pass

    def update_counter(self, tracks):
        for track in tracks:

            if(track.class_name == "person"):
                continue

            if(str(track.track_id) not in self.tracks.keys()):
                pos = self.calculate_position(track.coordinates)
                side = (self.line["delta_x"] * (pos[1] - self.line["endpt1"][1])) - (self.line["delta_y"] * (pos[0] - self.line["endpt1"][0]))
                if side != 0: self.tracks[str(track.track_id)] = side / abs(side) 
            else:
                new_pos = self.calculate_position(track.coordinates)
                new_side = (self.line["delta_x"] * (new_pos[1] - self.line["endpt1"][1])) - (self.line["delta_y"] * (new_pos[0] - self.line["endpt1"][0]))
                if(new_side > 0 and self.tracks[str(track.track_id)] < 0):
                    self.counter -= 1
                elif(new_side < 0 and self.tracks[str(track.track_id)] > 0):
                    self.counter += 1
                if new_side != 0: self.tracks[str(track.track_id)] = new_side / abs(new_side)  

            pass
        pass

    #center point
    def calculate_position(self, coordinates):
        x = (coordinates[0] + coordinates[2]) / 2
        y = (coordinates[1] + coordinates[3]) / 2
        pos = (x, y)
        return pos

    def annotate_counter(self, frame):
        cv2.line(frame, self.line["endpt1"], self.line["endpt2"], (0,0,255), thickness=5, lineType=cv2.LINE_8, shift=0)
        label = "NET: " + str(self.counter)
        cv2.putText(frame, label, (self.line["endpt1"][0],self.line["endpt1"][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        return frame


    pass