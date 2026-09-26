import cv2

from app.services.camera_service import get_camera_by_id
from app.services.detection_service import DetectionService
from vision.camera import open_camera
from vision.pipeline import PersonnelTrackingPipeline


# =====================================
# Caméra
# =====================================

camera = get_camera_by_id(2)

if camera is None:

    raise RuntimeError(
        "Caméra introuvable."
    )


cap = open_camera(camera)


# =====================================
# Pipeline
# =====================================

pipeline = PersonnelTrackingPipeline(
    dataset_path="dataset/faces",
    yolo_model="yolo11n.pt",
    recognition_threshold=0.45
)
detection_service = DetectionService(
    cooldown_seconds=10
)

# =====================================
# Boucle
# =====================================

while True:

    ret, frame = cap.read()

    if not ret:
        break


    result = pipeline.process_frame(
        frame
    )

    for detection in pipeline.last_detections:

        print("DETECTION PIPELINE :", detection)

        identity = detection["employee_id"]

        employee_id = detection_service.get_employee_id_by_identity(
            identity
        )

        if employee_id is None:
            print(
                f"[WARNING] Employee not found: {identity}"
            )
            continue

        detection_service.record_detection(
            employee_id=employee_id,
            camera_id=2
        )

    cv2.imshow(
        "Personnel Tracking",
        result
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()

cv2.destroyAllWindows()