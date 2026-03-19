from ultralytics import YOLO

class Detector:
    def __init__(self, weights='yolov8n.pt', conf=0.35, iou=0.5):
        self.model = YOLO(weights)
        self.conf = conf
        self.iou = iou

    def track(self, frame):
        return self.model.track(source=frame, persist=True, conf=self.conf, iou=self.iou, verbose=False)
