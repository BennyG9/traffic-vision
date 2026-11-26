import numpy as np
from scipy.optimize import linear_sum_assignment
from .IoU import IoU

def association(tracks, detections, matching_threshold):

    # number of tracks x number of detected objects
    num_tracks = len(tracks)
    num_objects = len(detections["boxes"])
    IoU_matrix = np.zeros((num_tracks, num_objects))

    #empty cases
    if(num_tracks == 0): return [], [], list(range(num_objects))
    if(num_objects == 0): return [], list(range(num_tracks)), []

    #calculate IoU matrix
    for i in range(num_tracks):
        tracking_coordinates = tracks[i].estimate_new_box()
        for j in range(num_objects):
            IoU_matrix[i,j] = IoU(tracking_coordinates, detections["boxes"][j]["coordinates"])

    cost_matrix = 1 - IoU_matrix
    cost_matrix[IoU_matrix < matching_threshold] = 1e6

    #optimal pairings from Hungarian algorithm
    track_indices, obj_indices = linear_sum_assignment(cost_matrix)

    #find matches based on given threshold
    matches = []
    for i in range(len(track_indices)):
        track_index = track_indices[i]
        obj_index = obj_indices[i]

        if(IoU_matrix[track_index, obj_index] >= matching_threshold):
            matches.append({
                "track_index": track_index,
                "object_index": obj_index
            })
        pass


    #find missed tracks
    matched_tracks = {match["track_index"] for match in matches}
    unmatched_tracks = [i for i in range(num_tracks) if(i not in matched_tracks)]

    #find missed objects
    matched_objects = {match["object_index"] for match in matches}
    unmatched_objects = [i for i in range(num_objects) if(i not in matched_objects)]

    return matches, unmatched_tracks, unmatched_objects