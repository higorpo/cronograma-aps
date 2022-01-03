
from __future__ import annotations
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.Atividade import Atividade


class Anotacao:

    def __init__(self, anotacao: str, atividade: Atividade):
        self.__id = uuid.uuid4()
        self.__anotacao = anotacao
        self.__atividade = atividade

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def anotacao(self) -> str:
        return self.__anotacao

    @anotacao.setter
    def anotacao(self, anotacao: str):
        self.__anotacao = anotacao

    @property
    def atividade(self) -> str:
        return self.__atividade
