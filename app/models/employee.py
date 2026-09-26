from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:
    id: Optional[int]
    matricule: str
    nom: str
    prenom: str
    face_embeddings: Optional[str] = None