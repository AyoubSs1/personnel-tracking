from ultralytics import YOLO


class PersonDetector:

    def __init__(self, model_path):

        self.model = YOLO(model_path)


    def track(self, frame):

        results = self.model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            classes=[0],
            imgsz=320,
            conf=0.4,
            verbose=False
        )

        return results[0]