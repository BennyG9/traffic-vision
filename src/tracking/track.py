import numpy as np

class Track():

    MAX_MISSED = 15

    def __init__(self, track_id, class_id, class_name, init_coordinates, init_confidence):
        #class init
        self.track_id = track_id
        self.class_id = class_id
        self.class_name = class_name

        #initialize tracker variables 
        self.coordinates = init_coordinates
        self.last_coordinates = init_coordinates
        self.confidence = init_confidence

        #save starting point
        self.starting_coordinates = init_coordinates

        #initialize tracking data dec
        self.age = 1
        self.hits = [1]
        self.missed_frames = 0
        pass


    #update information when track is matched with a detected object
    def log_hit(self, new_coordinates, new_confidence):
        self.last_coordinates = self.coordinates
        self.coordinates = new_coordinates
        self.confidence = new_confidence 
        self.age += 1
        self.hits.append(self.age)
        self.missed_frames = 0
        pass

    #update every frame track is not matched with a detected object
    def log_miss(self):
        self.missed_frames += 1
        self.age += 1
        pass


    #just return current box for now
    def estimate_new_box(self):

        #fallback when not enough data to extrapolate new coordiantes 
        if(len(self.hits) < 2):
            return self.coordinates

        #change in coordiantes over change in frames
        current = np.array(self.coordinates, dtype=float)
        last = np.array(self.last_coordinates, dtype=float)
        dxyxy_df = (current - last) / (self.hits[-1] - self.hits[-2])

        #we are checking every frame, df = 1
        df = 1

        return current + (df * dxyxy_df)

    pass