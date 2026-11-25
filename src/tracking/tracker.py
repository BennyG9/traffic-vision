from .association import association

class Tracker():

    def __init__(self):
        self.tracks = []
        pass


    def update(self, detections):

        association(self.tracks, detections)

        pass

    pass