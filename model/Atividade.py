import uuid
import datetime
from typing import List
from model.Tag import Tag
from model.Anotacao import Anotacao
from model.Disciplina import Disciplina
from utils.exceptions import NotFound


class Atividade:

    def __init__(self, nome: str, disciplina: Disciplina, grauDificuldade: str, prazoEntrega: datetime):
        self.__id = uuid.uuid4()
        self.__nome = nome
        self.__disciplina = disciplina
        self.__grauDificuldade = grauDificuldade
        self.__prazoEntrega = prazoEntrega
        self.__concluidaEm = None
        self.__tag = None
        self.__anotacoes: List[Anotacao] = list()

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: nome):
        self.__nome = nome

    @property
    def disciplina(self) -> datetime:
        return self.__disciplina

    @property
    def grauDificuldade(self) -> str:
        return self.__grauDificuldade

    @grauDificuldade.setter
    def grauDificuldade(self, grauDificuldade: Tag):
        self.__grauDificuldade = grauDificuldade

    @property
    def prazoEntrega(self) -> datetime:
        return self.__prazoEntrega

    @prazoEntrega.setter
    def prazoEntrega(self, prazoEntrega: Tag):
        self.__prazoEntrega = prazoEntrega

    @property
    def isConcluida(self) -> bool:
        return self.__concluidaEm is not None

    @property
    def concluidaEm(self) -> datetime:
        return self.__concluidaEm

    @concluidaEm.setter
    def concluidaEm(self, concluidaEm: str):
        self.__concluidaEm = concluidaEm

    @property
    def tag(self) -> Tag:
        return self.__tag

    @tag.setter
    def tag(self, tag: Tag):
        self.__tag = tag

    @property
    def anotacoes(self) -> List[Anotacao]:
        return self.__anotacoes

    def addAnotacao(self, texto_anotacao: str):
        self.__anotacoes.push(Anotacao(texto_anotacao, self))

    def deleteAnotacao(self, anotacao: Anotacao):
        if anotacao in self.__anotacoes:
            self.__anotacoes.remove(anotacao)
        else:
            raise NotFound()
