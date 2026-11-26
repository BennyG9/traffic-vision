import numpy as np

class Track():

    MAX_MISSED = 25

    def __init__(self, track_id, class_id, class_name, init_coordinates, init_confidence):
        #class init
        self.track_id = track_id
        self.class_id = class_id
        self.class_name = class_name

        #initialize tracker variables 
        self.coordinates = init_coordinates
        self.last_coordinates = init_coordinates
        self.confidence = init_confidence
        self.velocity = np.zeros(4, dtype=float)
        self.alpha = 0.8

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

        #calculate velocity 
        current_coordinates = np.array(self.coordinates, dtype=float)
        previous_coordinates = np.array(self.last_coordinates, dtype=float)
        v_new = (current_coordinates - previous_coordinates) / (self.hits[-1] - self.hits[-2])
        self.velocity = (self.alpha * v_new) + (1 - self.alpha)*self.velocity
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

        current = np.array(self.coordinates)

        #we are checking every frame, df = 1
        df = (self.age + 1) - self.hits[-1]

        return current + (df * self.velocity)

    pass