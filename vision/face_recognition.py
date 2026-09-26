import numpy as np
from insightface.app import FaceAnalysis


class FaceRecognizer:

    def __init__(self):

        self.app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"]
        )

        self.app.prepare(
            ctx_id=-1,
            det_size=(320, 320)
        )

    def get_faces(self, frame):

        return self.app.get(frame)

    def get_embedding(self, face):

        embedding = face.embedding

        embedding = embedding / np.linalg.norm(
            embedding
        )

        return embedding

    def compare(self, embedding1, embedding2):

        embedding1 = embedding1 / np.linalg.norm(
            embedding1
        )

        embedding2 = embedding2 / np.linalg.norm(
            embedding2
        )

        return float(
            np.dot(embedding1, embedding2)
        )