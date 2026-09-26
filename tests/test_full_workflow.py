import cv2
import time

from vision.pipeline import PersonnelTrackingPipeline
from app.services.detection_service import DetectionService
from app.services.location_service import LocationService
from app.services.unknown_detection_service import UnknownDetectionService


# ============================================================
# CONFIGURATION
# ============================================================

WEBCAM_SOURCE = 0

PHONE_SOURCE = "http://192.168.11.103:8080/video"

MODEL_PATH = "yolo11n.pt"

WEBCAM_CAMERA_ID = 1
PHONE_CAMERA_ID = 2


# ============================================================
# SERVICES
# ============================================================

unknown_detection_service = UnknownDetectionService()
detection_service = DetectionService(cooldown_seconds=10)
location_service = LocationService()


# ============================================================
# PIPELINE
# ============================================================

pipeline = PersonnelTrackingPipeline(
   yolo_model=MODEL_PATH
)


# ============================================================
# FONCTION DE TEST D'UNE CAMERA
# ============================================================

def test_camera(camera_source, camera_id, camera_name, location):
    print("\n" + "=" * 60)
    print(f"CAMERA : {camera_name}")
    print(f"LOCATION : {location}")
    print(f"CAMERA ID : {camera_id}")
    print("=" * 60)

    cap = cv2.VideoCapture(camera_source)

    if not cap.isOpened():
        print("[ERROR] Impossible d'ouvrir la caméra.")
        return False

    print("[OK] Camera ouverte.")
    print("Place-toi devant la caméra.")
    print("Appuie sur 'q' pour terminer ce test.")

    detection_recorded = False

    while True:

        ret, frame = cap.read()

        if not ret:
            print("[ERROR] Impossible de lire le frame.")
            break

        # Traitement IA
        pipeline.process_frame(frame)

        # Récupérer les personnes reconnues
        for detection in pipeline.last_detections:

            identity = detection["employee_id"]

            # =========================================
            # PERSONNE INCONNUE
            # =========================================

            if identity == "UNKNOWN":

                unknown_detection_service.notify(
                    camera_id=camera_id,
                    camera_name=camera_name,
                    location=location,
                    track_id=detection["track_id"]
                )

                continue

            # =========================================
            # EMPLOYE CONNU
            # =========================================

            employee_id = (
                detection_service
                .get_employee_id_by_identity(identity)
            )

            if employee_id is None:

                continue

            detection_service.record_detection(
                employee_id=employee_id,
                camera_id=camera_id
            )

        # Affichage
        cv2.imshow(
            f"{camera_name} - {location}",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    if detection_recorded:
        print("\n[OK] Detection enregistree dans la DB.")
    else:
        print("\n[WARNING] Aucune nouvelle detection enregistree.")

    return detection_recorded


# ============================================================
# WORKFLOW COMPLET
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("       PERSONNEL TRACKING - FULL WORKFLOW TEST")
    print("=" * 60)

    # --------------------------------------------------------
    # ETAPE 1 : WEBCAM
    # --------------------------------------------------------

    print("\n")
    print("ETAPE 1/3 - WEBCAM PC")
    print("-" * 60)

    test_camera(
        camera_source=WEBCAM_SOURCE,
        camera_id=WEBCAM_CAMERA_ID,
        camera_name="Webcam PC",
        location="Bureau informatique"
    )

    print("\n")
    print("Webcam termine.")
    print("Maintenant passe devant le TELEPHONE.")

    time.sleep(2)

    # --------------------------------------------------------
    # ETAPE 2 : TELEPHONE
    # --------------------------------------------------------

    print("\n")
    print("ETAPE 2/3 - TELEPHONE")
    print("-" * 60)

    test_camera(
        camera_source=PHONE_SOURCE,
        camera_id=PHONE_CAMERA_ID,
        camera_name="Smartphone",
        location="Salle de réunion"
    )

    # --------------------------------------------------------
    # ETAPE 3 : LOCATION
    # --------------------------------------------------------

    print("\n")
    print("ETAPE 3/3 - DERNIERE LOCALISATION")
    print("-" * 60)

    # Employee Ayoub = ID 1
    result = location_service.get_last_location(
        employee_id=1
    )

    if result is None:

        print("[ERROR] Aucune detection trouvee.")

    else:

        print("\n===== LAST LOCATION =====")

        print(f"Employee ID : {result['employee_id']}")
        print(f"Matricule   : {result['matricule']}")
        print(f"Nom         : {result['nom']}")
        print(f"Prénom      : {result['prenom']}")
        print(f"Caméra      : {result['camera_name']}")
        print(f"Localisation: {result['location']}")
        print(f"Date        : {result['date']}")
        print(f"Heure       : {result['heure']}")

        # Vérification automatique
        if result["camera_id"] == PHONE_CAMERA_ID:

            print("\n[OK] WORKFLOW COMPLET REUSSI")
            print(
                "La dernière localisation de l'employé "
                "est bien celle du téléphone."
            )

        else:

            print("\n[WARNING]")
            print(
                "La dernière localisation n'est pas "
                "celle du téléphone."
            )


if __name__ == "__main__":
    main()