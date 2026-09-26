from datetime import datetime, timedelta
from app.database.connection import get_connection


class DetectionService:

    def __init__(self, cooldown_seconds=10):
        self.cooldown = timedelta(seconds=cooldown_seconds)
        self.last_detections = {}

    def get_employee_id_by_identity(self, identity):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id
                FROM employees
                WHERE LOWER(prenom || '_' || nom) = LOWER(?)
                """,
                (identity,)
            )

            row = cursor.fetchone()

            if row:
                return row["id"]

            return None

        finally:
            conn.close()

    def record_detection(self, employee_id, camera_id):

        now = datetime.now()
        key = (employee_id, camera_id)

        last_time = self.last_detections.get(key)

        if last_time is not None:
            elapsed = now - last_time

            if elapsed < self.cooldown:
                return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO detections (
                    employee_id,
                    camera_id,
                    date,
                    heure
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    employee_id,
                    camera_id,
                    now.date().isoformat(),
                    now.time().isoformat()
                )
            )

            conn.commit()

            self.last_detections[key] = now

            print(
                f"[DETECTION] "
                f"Employee={employee_id} "
                f"Camera={camera_id} "
                f"Date={now.date()} "
                f"Time={now.time()}"
            )

            return True

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()