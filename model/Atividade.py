import uuid
import datetime
from typing import List
from model.Tag import Tag
# from model.Anotacao import Anotacao
from model.Disciplina import Disciplina
from utils.exceptions import NotFound


class Atividade:

    def __init__(self, nome: str, disciplina: Disciplina, grau_dificuldade: str, prazo_entrega: datetime):
        self.__id = uuid.uuid4()
        self.__nome = nome
        self.__disciplina = disciplina
        self.__grau_dificuldade = grau_dificuldade
        self.__prazo_entrega = prazo_entrega
        self.__concluidaEm = None
        self.__tag = None
        self.__anotacoes: list()

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
    def disciplina(self) -> Disciplina:
        return self.__disciplina

    @property
    def grau_dificuldade(self) -> str:
        return self.__grau_dificuldade

    @grau_dificuldade.setter
    def grau_dificuldade(self, grau_dificuldade: str):
        self.__grau_dificuldade = grau_dificuldade

    @property
    def prazo_entrega(self) -> datetime:
        return self.__prazo_entrega.strftime('%d/%m/%Y')

    @prazo_entrega.setter
    def prazo_entrega(self, prazo_entrega: datetime):
        self.__prazo_entrega = prazo_entrega

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

    # @property
    # def anotacoes(self) -> List[Anotacao]:
    #     return self.__anotacoes

    # def addAnotacao(self, texto_anotacao: str):
    #     self.__anotacoes.push(Anotacao(texto_anotacao, self))

    # def deleteAnotacao(self, anotacao: Anotacao):
    #     if anotacao in self.__anotacoes:
    #         self.__anotacoes.remove(anotacao)
    #     else:
    #         raise NotFound()
