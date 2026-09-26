import cv2

from app.services.camera_service import get_camera_by_id
from vision.camera import open_camera
from vision.detector import PersonDetector


# =====================================
# 1. Caméra
# =====================================

camera = get_camera_by_id(1)

if camera is None:

    raise RuntimeError(
        "Caméra introuvable."
    )


cap = open_camera(camera)


# =====================================
# 2. YOLO + ByteTrack
# =====================================

detector = PersonDetector(
    "yolo11n.pt"
)


# =====================================
# 3. Boucle
# =====================================

while True:

    ret, frame = cap.read()

    if not ret:
        break


    # =================================
    # Tracking
    # =================================

    result = detector.track(frame)


    # =================================
    # Dessiner
    # =================================

    annotated_frame = frame.copy()


    if result.boxes is not None:

        boxes = result.boxes


        for i in range(len(boxes)):

            # Bounding box

            x1, y1, x2, y2 = (
                boxes.xyxy[i]
                .cpu()
                .numpy()
                .astype(int)
            )


            # Confidence

            confidence = float(
                boxes.conf[i]
            )


            # Track ID

            if boxes.id is not None:

                track_id = int(
                    boxes.id[i]
                    .cpu()
                    .item()
                )

            else:

                track_id = -1


            # =================================
            # Bounding box
            # =================================

            cv2.rectangle(
                annotated_frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )


            # =================================
            # Label
            # =================================

            label = (
                f"ID: {track_id} "
                f"{confidence:.2f}"
            )


            cv2.putText(
                annotated_frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )


    # =================================
    # Affichage
    # =================================

    cv2.imshow(
        "ByteTrack Test",
        annotated_frame
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()

cv2.destroyAllWindows()