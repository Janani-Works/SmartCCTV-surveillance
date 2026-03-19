''' PERSON_CLASS_NAME = 'person'
VEHICLE_CLASS_NAMES = {'car', 'truck', 'bus', 'motorbike', 'bicycle'}

def bbox_wh(xyxy):
    x1, y1, x2, y2 = [float(v) for v in xyxy]
    return max(0.0, x2 - x1), max(0.0, y2 - y1)

def bbox_center(xyxy):
    x1, y1, x2, y2 = [float(v) for v in xyxy]
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

def person_likely_fallen(xyxy, frame_h):
    w, h = bbox_wh(xyxy)
    if h <= 0:
        return False
    aspect = w / h
    _, y1, _, y2 = [float(v) for v in xyxy]
    near_ground = y2 > frame_h * 0.75
    return aspect > 1.35 and near_ground

def vehicle_stopped(avg_speed_px_per_frame, frames_static, speed_thr=1.5, frames_thr=30):
    return avg_speed_px_per_frame < speed_thr and frames_static >= frames_thr

def crowding(num_persons, frame_area, density_thr=0.00008):
    density = num_persons / max(1, frame_area)
    return density > density_thr
'''

#New
import math

# Class name constants
PERSON_CLASS_NAME = 'person'
VEHICLE_CLASS_NAMES = {'car', 'truck', 'bus', 'motorbike', 'bicycle'}

# ---------------- Existing helper functions ----------------
def bbox_wh(xyxy):
    x1, y1, x2, y2 = [float(v) for v in xyxy]
    return max(0.0, x2 - x1), max(0.0, y2 - y1)

def bbox_center(xyxy):
    x1, y1, x2, y2 = [float(v) for v in xyxy]
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

def person_likely_fallen(xyxy, frame_h):
    w, h = bbox_wh(xyxy)
    if h <= 0:
        return False
    aspect = w / h
    _, y1, _, y2 = [float(v) for v in xyxy]
    near_ground = y2 > frame_h * 0.65
    return aspect > 1.1 and near_ground

def vehicle_stopped(avg_speed_px_per_frame, frames_static, speed_thr=1.5, frames_thr=30):
    return avg_speed_px_per_frame < speed_thr and frames_static >= frames_thr

def crowding(num_persons, frame_area, density_thr=0.00008):
    density = num_persons / max(1, frame_area)
    return density > density_thr

# ---------------- New collision detection function ----------------
def vehicles_collided(vehicle_centers, distance_thr=40):
    """
    Checks if any two vehicles are too close (possible collision).
    vehicle_centers: list of (x, y) tuples
    distance_thr: distance threshold for collision (in pixels)
    """
    for i in range(len(vehicle_centers)):
        for j in range(i + 1, len(vehicle_centers)):
            dist = math.dist(vehicle_centers[i], vehicle_centers[j])
            if dist < distance_thr:
                return True
    return False 