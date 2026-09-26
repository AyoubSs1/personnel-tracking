import cv2
import time

from app.services.camera_service import get_camera_by_id
from vision.camera import open_camera
from vision.pipeline import PersonnelTrackingPipeline


# =====================================
# 1. Caméra
# =====================================

camera = get_camera_by_id(1)

if camera is None:
    raise RuntimeError("Caméra introuvable.")


cap = open_camera(camera)


# =====================================
# 2. Pipeline
# =====================================

pipeline = PersonnelTrackingPipeline(
    dataset_path="dataset/faces",
    yolo_model="yolo11n.pt",
    recognition_threshold=0.45
)


# =====================================
# 3. Variables optimisation
# =====================================

frame_count = 0

DETECTION_INTERVAL = 8

last_result = None

prev_time = time.time()


# =====================================
# 4. Boucle
# =====================================

while True:

    ret, frame = cap.read()

    if not ret:
        print("Impossible de lire la frame.")
        break

    frame_count += 1


    # =================================
    # YOLO + Face Recognition
    # seulement toutes les 5 frames
    # =================================

    if frame_count % DETECTION_INTERVAL == 0:

        last_result = pipeline.process_frame(
            frame
        )


    # =================================
    # Affichage
    # =================================

    if last_result is not None:

        display_frame = last_result

    else:

        display_frame = frame


    # =================================
    # FPS
    # =================================

    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time


    cv2.putText(
        display_frame,
        f"FPS: {fps:.1f}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )


    cv2.imshow(
        "Personnel Tracking",
        display_frame
    )


    # =================================
    # Quitter
    # =================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()

cv2.destroyAllWindows()