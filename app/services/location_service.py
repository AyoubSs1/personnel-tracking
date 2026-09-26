from app.database.connection import get_connection


class LocationService:

    def get_last_location(self, employee_id):

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    e.id AS employee_id,
                    e.matricule,
                    e.nom,
                    e.prenom,
                    c.id AS camera_id,
                    c.camera_name,
                    c.location,
                    d.date,
                    d.heure
                FROM detections d
                JOIN employees e
                    ON e.id = d.employee_id
                JOIN cameras c
                    ON c.id = d.camera_id
                WHERE e.id = ?
                ORDER BY d.date DESC, d.heure DESC
                LIMIT 1
                """,
                (employee_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return dict(row)

        finally:
            conn.close()