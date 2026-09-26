from app.services.location_service import LocationService


service = LocationService()

result = service.get_last_location(employee_id=1)

print("\n===== LAST LOCATION =====")

if result is None:
    print("Aucune détection trouvée.")

else:
    print(f"Employee ID : {result['employee_id']}")
    print(f"Matricule   : {result['matricule']}")
    print(f"Nom         : {result['nom']}")
    print(f"Prénom      : {result['prenom']}")
    print(f"Caméra      : {result['camera_name']}")
    print(f"Localisation: {result['location']}")
    print(f"Date        : {result['date']}")
    print(f"Heure       : {result['heure']}")