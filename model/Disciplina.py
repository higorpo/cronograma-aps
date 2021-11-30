import uuid
from model.PeriodoLetivo import PeriodoLetivo


class Disciplina:

    def __init__(self, nome: str, periodo_letivo: PeriodoLetivo):
        self.__id = uuid.uuid4()
        self.__nome = nome
        self.__periodo_letivo = periodo_letivo

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
    def periodo_letivo(self) -> PeriodoLetivo:
        return self.__periodo_letivo

    @periodo_letivo.setter
    def periodo_letivo(self, periodo_letivo: PeriodoLetivo):
        self.__periodo_letivo = periodo_letivo
