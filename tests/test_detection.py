import cv2
import time

from vision.camera import open_camera
from vision.detector import PersonDetector

from app.services.camera_service import get_camera_by_id


# =========================
# Récupérer la caméra
# =========================

camera = get_camera_by_id(1)

if camera is None:
    raise RuntimeError("Caméra introuvable.")


# =========================
# Ouvrir la caméra
# =========================

cap = open_camera(camera)


# =========================
# Charger YOLO
# =========================

detector = PersonDetector(
    "yolo11n.pt"
)


# =========================
# Boucle vidéo
# =========================
prev_time = time.time()
frame_count = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    if frame_count % 3 == 0:

        results = detector.detect(frame)

        annotated_frame = results.plot()

        cv2.imshow(
            "YOLO - Person Detection",
            annotated_frame
        )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


    # Quitter avec Q
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# =========================
# Libérer les ressources
# =========================

cap.release()
cv2.destroyAllWindows()