import uuid

from dao.AbstractDAO import DAO
from model.Atividade import Atividade


class AtividadeDAO(DAO):
    def __init__(self):
        super().__init__('dao/store/atividade.pkl')

    def add(self, atividade: Atividade):
        if ((atividade is not None) and isinstance(atividade, Atividade) and isinstance(atividade.id, uuid.UUID)):
            super().add(atividade.id, atividade)

    def remove(self, atividade: Atividade):
        if ((atividade is not None) and isinstance(atividade, Atividade) and isinstance(atividade.id, uuid.UUID)):
            super().remove(atividade.id)
