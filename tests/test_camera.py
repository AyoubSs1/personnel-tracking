from app.models.camera import Camera

from app.services.camera_service import (
    create_camera,
    get_all_cameras
)


# =========================
# Webcam PC
# =========================

camera = Camera(
    id=None,
    camera_name="Webcam PC",
    location="Bureau informatique",
    source="0",
    source_type="webcam"
)

camera_id = create_camera(camera)

print("Webcam créée :", camera_id)


# =========================
# Smartphone
# =========================

camera2 = Camera(
    id=None,
    camera_name="Smartphone",
    location="Salle de réunion",
    source="http://192.168.1.20:8080/video",
    source_type="ip"
)

camera2_id = create_camera(camera2)

print("Smartphone créé :", camera2_id)


# =========================
# Affichage
# =========================

cameras = get_all_cameras()

print("\nCaméras :")

for camera in cameras:

    print(
        f"ID: {camera['id']} | "
        f"Nom: {camera['camera_name']} | "
        f"Emplacement: {camera['location']} | "
        f"Source: {camera['source']} | "
        f"Type: {camera['source_type']}"
    )