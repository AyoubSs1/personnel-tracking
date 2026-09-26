from app.services.detection_service import DetectionService


service = DetectionService(
    cooldown_seconds=10
)


print(
    service.record_detection(
        employee_id=1,
        camera_id=1
    )
)


print(
    service.record_detection(
        employee_id=1,
        camera_id=1
    )
)