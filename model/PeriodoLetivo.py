import uuid


class PeriodoLetivo:

    def __init__(self, nome: str):
        self.__id = uuid.uuid4()
        self.__nome = nome

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome
