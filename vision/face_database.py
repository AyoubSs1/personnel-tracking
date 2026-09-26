import os
import cv2
import numpy as np

from vision.face_recognition import FaceRecognizer


class FaceDatabase:

    def __init__(self, dataset_path):

        self.dataset_path = dataset_path
        self.recognizer = FaceRecognizer()

        self.embeddings = {}

    def build(self):

        print("Construction de la base des visages...")

        for employee_id in os.listdir(self.dataset_path):

            employee_path = os.path.join(
                self.dataset_path,
                employee_id
            )

            if not os.path.isdir(employee_path):
                continue

            employee_embeddings = []

            for filename in os.listdir(employee_path):

                image_path = os.path.join(
                    employee_path,
                    filename
                )

                image = cv2.imread(image_path)

                if image is None:
                    print(
                        f"Impossible de lire : {image_path}"
                    )
                    continue

                faces = self.recognizer.get_faces(image)

                if len(faces) == 0:

                    print(
                        f"Aucun visage trouvé : {image_path}"
                    )

                    continue

                if len(faces) > 1:

                    print(
                        f"Plusieurs visages trouvés : "
                        f"{image_path}"
                    )

                face = faces[0]

                embedding = self.recognizer.get_embedding(
                    face
                )

                employee_embeddings.append(
                    embedding
                )

            if employee_embeddings:

                mean_embedding = np.mean(
                    employee_embeddings,
                    axis=0
                )

                mean_embedding = (
                    mean_embedding /
                    np.linalg.norm(mean_embedding)
                )

                self.embeddings[employee_id] = (
                    mean_embedding
                )

                print(
                    f"{employee_id} : "
                    f"{len(employee_embeddings)} "
                    f"images utilisées"
                )

        print(
            f"\nBase créée : "
            f"{len(self.embeddings)} employés"
        )

        return self.embeddings