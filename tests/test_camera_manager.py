from app.services.camera_manager import CameraManager


manager = CameraManager()

print("\n===== CAMERAS =====")

cameras = manager.get_all_cameras()

for camera in cameras:
    print(
        f"{camera['id']} | "
        f"{camera['camera_name']} | "
        f"{camera['location']} | "
        f"{camera['source']} | "
        f"{camera['source_type']}"
    )


print("\n===== TEST CAMERA 1 =====")

cap, camera = manager.open_camera(1)

print(f"Nom        : {camera['camera_name']}")
print(f"Localisation : {camera['location']}")
print(f"Source     : {camera['source']}")
print(f"Type       : {camera['source_type']}")

cap.release()

print("[OK] Camera 1 ouverte.")


print("\n===== TEST CAMERA 2 =====")

cap, camera = manager.open_camera(2)

print(f"Nom        : {camera['camera_name']}")
print(f"Localisation : {camera['location']}")
print(f"Source     : {camera['source']}")
print(f"Type       : {camera['source_type']}")

cap.release()

print("[OK] Camera 2 ouverte.")