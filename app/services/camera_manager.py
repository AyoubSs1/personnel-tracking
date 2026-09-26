import cv2
from app.database.connection import get_connection


class CameraManager:

    def get_camera(self, camera_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, camera_name, location, source, source_type
                FROM cameras
                WHERE id = ?
                """,
                (camera_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return dict(row)

        finally:
            conn.close()

    def get_all_cameras(self):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, camera_name, location, source, source_type
                FROM cameras
                ORDER BY id
                """
            )

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()

    def open_camera(self, camera_id):
        camera = self.get_camera(camera_id)

        if camera is None:
            raise ValueError(
                f"Camera {camera_id} introuvable."
            )

        source = camera["source"]
        source_type = camera["source_type"]

        if source_type == "webcam":
            source = int(source)

        cap = cv2.VideoCapture(source)

        if not cap.isOpened():
            raise RuntimeError(
                f"Impossible d'ouvrir la caméra "
                f"{camera['camera_name']}"
            )

        return cap, camera