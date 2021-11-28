import uuid

from dao.AbstractDAO import DAO
from model.Disciplina import Disciplina


class DisciplinaDAO(DAO):
    def __init__(self):
        super().__init__('dao/store/disciplina.pkl')

    def add(self, disciplina: Disciplina):
        if ((disciplina is not None) and isinstance(disciplina, Disciplina) and isinstance(disciplina.id, uuid.UUID)):
            super().add(disciplina.id, disciplina)

    def remove(self, disciplina: Disciplina):
        if ((disciplina is not None) and isinstance(disciplina, Disciplina) and isinstance(disciplina.id, uuid.UUID)):
            super().remove(disciplina.id)
