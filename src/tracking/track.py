class Track():

    MAX_MISSED = 100

    def __init__(self, track_id, class_id, class_name, init_coordinates, init_confidence):
        #class init
        self.track_id = track_id
        self.class_id = class_id
        self.class_name = class_name

        #initialize tracker variables 
        self.coordinates = init_coordinates
        self.confidence = init_confidence

        #save starting point
        self.starting_coordinates = init_coordinates

        #initialize tracking data dec
        self.age = 1
        self.hits = 1
        self.missed_frames = 0
        pass


    #update information when track is matched with a detected object
    def log_hit(self, new_coordinates, new_confidence):
        self.coordinates = new_coordinates
        self.confidence = new_confidence 
        self.hits += 1
        self.age += 1
        self.missed_frames = 0
        pass

    #update every frame track is not matched with a detected object
    def log_miss(self):
        self.missed_frames += 1
        self.age += 1
        pass


    #just return current box for now
    def estimate_new_box(self):
        return self.coordinates

    pass