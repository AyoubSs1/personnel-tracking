from app.database.connection import get_connection
from app.models.camera import Camera


from app.database.connection import get_connection
from app.models.camera import Camera


def create_camera(camera: Camera):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cameras (
            camera_name,
            location,
            source,
            source_type
        )
        VALUES (?, ?, ?, ?)
    """, (
        camera.camera_name,
        camera.location,
        camera.source,
        camera.source_type
    ))

    conn.commit()

    camera_id = cursor.lastrowid

    conn.close()

    return camera_id
def get_all_cameras():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM cameras
        ORDER BY id
    """)

    cameras = cursor.fetchall()

    conn.close()

    return cameras
def get_camera_by_id(camera_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM cameras
        WHERE id = ?
    """, (camera_id,))

    camera = cursor.fetchone()

    conn.close()

    return camera
def update_camera(
    camera_id: int,
    camera_name: str,
    location: str,
    source: str
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cameras
        SET camera_name = ?,
            location = ?,
            source = ?
        WHERE id = ?
    """, (
        camera_name,
        location,
        source,
        camera_id
    ))

    conn.commit()

    conn.close()

def delete_camera(camera_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM cameras
        WHERE id = ?
    """, (camera_id,))

    conn.commit()

    conn.close()