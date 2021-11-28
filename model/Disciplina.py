import uuid
from model.PeriodoLetivo import PeriodoLetivo


class Disciplina:

    def __init__(self, nome: str, periodoLetivo: PeriodoLetivo):
        self.__id = uuid.uuid4()
        self.__nome = nome
        self.__periodoLetivo = periodoLetivo

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def periodoLetivo(self) -> PeriodoLetivo:
        return self.__periodoLetivo

    @periodoLetivo.setter
    def periodoLetivo(self, periodoLetivo: PeriodoLetivo):
        self.__periodoLetivo = periodoLetivo
