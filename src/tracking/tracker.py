from .association import association
from .track import Track

class Tracker():

    def __init__(self):
        self.tracks = []
        self.next_track_id = 0
        pass


    def update(self, detections):

        #object and track associations 
        matches, unmatched_tracks, unmatched_objects = association(self.tracks, detections, 0.5)

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