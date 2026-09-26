import numpy as np


class IdentityMatcher:

    def __init__(
        self,
        face_database,
        threshold=0.45
    ):

        self.face_database = face_database
        self.threshold = threshold

    def recognize(self, embedding):

        embedding = embedding / np.linalg.norm(
            embedding
        )

        best_employee = None
        best_similarity = -1

        for employee_id, reference_embedding in self.face_database.items():

            similarity = float(
                np.dot(
                    embedding,
                    reference_embedding
                )
            )

            if similarity > best_similarity:

                best_similarity = similarity
                best_employee = employee_id

        if best_similarity >= self.threshold:

            return {
                "employee_id": best_employee,
                "similarity": best_similarity
            }

        return {
            "employee_id": None,
            "similarity": best_similarity
        }