import cv2

from vision.face_recognition import FaceRecognizer
from vision.face_database import FaceDatabase
from vision.identity import IdentityMatcher


# ==========================================
# 1. Construire la base des visages
# ==========================================

dataset_path = "dataset/faces"

face_database_builder = FaceDatabase(
    dataset_path
)

face_database = face_database_builder.build()


if not face_database:

    raise RuntimeError(
        "La base des visages est vide."
    )


# ==========================================
# 2. Créer le matcher
# ==========================================

matcher = IdentityMatcher(
    face_database,
    threshold=0.45
)


# ==========================================
# 3. Charger le recognizer
# ==========================================

recognizer = FaceRecognizer()


# ==========================================
# 4. Charger une image de test
# ==========================================

image_path = "dataset/faces/Ayoub_Soussi/img1.jpeg"

image = cv2.imread(image_path)

if image is None:

    raise RuntimeError(
        f"Impossible de lire : {image_path}"
    )


# ==========================================
# 5. Détecter les visages
# ==========================================

faces = recognizer.get_faces(image)

print(
    f"\nNombre de visages détectés : {len(faces)}"
)


# ==========================================
# 6. Reconnaître les visages
# ==========================================

for face in faces:

    embedding = recognizer.get_embedding(
        face
    )

    result = matcher.recognize(
        embedding
    )

    print("\nRésultat :")

    print(
        "Employee ID :",
        result["employee_id"]
    )

    print(
        "Similarity :",
        result["similarity"]
    )