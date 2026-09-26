from app.database.connection import get_connection


def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    # ==========================================
    # Table detections
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            employee_id INTEGER NOT NULL,

            camera_id INTEGER NOT NULL,

            date TEXT NOT NULL,

            heure TEXT NOT NULL,

            FOREIGN KEY (employee_id)
                REFERENCES employees(id),

            FOREIGN KEY (camera_id)
                REFERENCES cameras(id)
        )
    """)

    conn.commit()

    conn.close()

    print("Database initialized successfully.")


if __name__ == "__main__":

    init_db()