import uuid

from dao.AbstractDAO import DAO
from model.Anotacao import Anotacao


class AnotacaoDAO(DAO):
    def __init__(self):
        super().__init__('dao/store/anotacao.pkl')

    def add(self, anotacao: Anotacao):
        if ((anotacao is not None) and isinstance(anotacao, Anotacao) and isinstance(anotacao.id, uuid.UUID)):
            super().add(anotacao.id, anotacao)

    def remove(self, anotacao: Anotacao):
        if ((anotacao is not None) and isinstance(anotacao, Anotacao) and isinstance(anotacao.id, uuid.UUID)):
            super().remove(anotacao.id)
