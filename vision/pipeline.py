import cv2

from vision.detector import PersonDetector
from vision.face_recognition import FaceRecognizer
from vision.face_database import FaceDatabase
from vision.identity import IdentityMatcher
from vision.track_identity import TrackIdentityManager


class PersonnelTrackingPipeline:

    def __init__(
        self,
        dataset_path="dataset/faces",
        yolo_model="yolo11n.pt",
        recognition_threshold=0.45
    ):

        print("Chargement de YOLO...")

        self.detector = PersonDetector(
            yolo_model
        )

        print(
            "Chargement de la reconnaissance faciale..."
        )

        self.face_recognizer = FaceRecognizer()

        print(
            "Construction de la base faciale..."
        )

        database_builder = FaceDatabase(
            dataset_path
        )

        face_database = database_builder.build()

        if not face_database:

            raise RuntimeError(
                "La base faciale est vide."
            )

        self.matcher = IdentityMatcher(
            face_database,
            threshold=recognition_threshold
        )

        # =====================================
        # Manager Track → Employee
        # =====================================

        self.track_manager = (
            TrackIdentityManager()
        )

        # =====================================
        # Dernières détections du frame
        # =====================================

        self.last_detections = []

        print("Pipeline prêt.")

    # =========================================================
    # PROCESS FRAME
    # =========================================================

    def process_frame(self, frame):

        self.last_detections = []

        annotated_frame = frame.copy()

        # =====================================
        # 1. YOLO + ByteTrack
        # =====================================

        result = self.detector.track(
            frame
        )

        if result.boxes is None:

            return annotated_frame

        boxes = result.boxes

        # =====================================
        # 2. Parcourir les personnes
        # =====================================

        for i in range(len(boxes)):

            # ---------------------------------
            # Bounding box
            # ---------------------------------

            x1, y1, x2, y2 = (
                boxes.xyxy[i]
                .cpu()
                .numpy()
                .astype(int)
            )

            # ---------------------------------
            # Confidence YOLO
            # ---------------------------------

            confidence = float(
                boxes.conf[i]
            )

            # ---------------------------------
            # Track ID
            # ---------------------------------

            if boxes.id is None:

                continue

            track_id = int(
                boxes.id[i]
                .cpu()
                .item()
            )

            # =================================
            # 3. Vérifier si Track déjà connu
            # =================================

            employee_id = (
                self.track_manager
                .get_identity(track_id)
            )

            # =================================
            # 4. Si Track pas encore connu
            # =================================

            if employee_id is None:

                employee_id = (
                    self.recognize_person(
                        frame,
                        x1,
                        y1,
                        x2,
                        y2
                    )
                )

                # ---------------------------------
                # EMPLOYE RECONNU
                # ---------------------------------

                if employee_id is not None:

                    # Mémoriser l'identité
                    self.track_manager.set_identity(
                        track_id,
                        employee_id
                    )

                    # Ajouter aux détections
                    self.last_detections.append({
                        "employee_id": employee_id,
                        "track_id": track_id,
                        "confidence": confidence,
                        "status": "known"
                    })

                # ---------------------------------
                # PERSONNE INCONNUE
                # ---------------------------------

                else:

                    self.last_detections.append({
                        "employee_id": "UNKNOWN",
                        "track_id": track_id,
                        "confidence": confidence,
                        "status": "unknown"
                    })

            # =================================
            # 5. Label
            # =================================

            if employee_id is not None:

                label = (
                    f"ID:{track_id} "
                    f"{employee_id}"
                )

            else:

                label = (
                    f"ID:{track_id} "
                    f"UNKNOWN"
                )

            # =================================
            # 6. Bounding box
            # =================================

            cv2.rectangle(
                annotated_frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # =================================
            # 7. Label background
            # =================================

            cv2.rectangle(
                annotated_frame,
                (x1, y1 - 30),
                (x1 + 220, y1),
                (0, 255, 0),
                -1
            )

            # =================================
            # 8. Label
            # =================================

            cv2.putText(
                annotated_frame,
                label,
                (x1 + 5, y1 - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2
            )

        return annotated_frame

    # =========================================================
    # RECOGNITION
    # =========================================================

    def recognize_person(
        self,
        frame,
        x1,
        y1,
        x2,
        y2
    ):

        # =====================================
        # Sécurité
        # =====================================

        h, w = frame.shape[:2]

        x1 = max(0, x1)
        y1 = max(0, y1)

        x2 = min(w, x2)
        y2 = min(h, y2)

        # =====================================
        # Crop personne
        # =====================================

        person_crop = frame[
            y1:y2,
            x1:x2
        ]

        if person_crop.size == 0:

            return None

        # =====================================
        # Détection visage
        # =====================================

        faces = (
            self.face_recognizer
            .get_faces(person_crop)
        )

        if len(faces) == 0:

            return None

        # =====================================
        # Premier visage
        # =====================================

        face = faces[0]

        # =====================================
        # Embedding
        # =====================================

        embedding = (
            self.face_recognizer
            .get_embedding(face)
        )

        # =====================================
        # Matching
        # =====================================

        result = self.matcher.recognize(
            embedding
        )

        # =====================================
        # Identité
        # =====================================

        if result is None:

            return None

        return result["employee_id"]