import uuid
import datetime
from model.Anotacao import Anotacao
from typing import List
from model.Tag import Tag
from model.Disciplina import Disciplina
from utils.exceptions import NotFound


class Atividade:

    def __init__(self, nome: str, disciplina: Disciplina, grau_dificuldade: str, prazo_entrega: datetime):
        self.__id = uuid.uuid4()
        self.__nome = nome
        self.__disciplina = disciplina
        self.__grau_dificuldade = grau_dificuldade
        self.__prazo_entrega = prazo_entrega
        self.__concluida_em = None
        self.__tag = None
        self.__anotacoes: list()
        self.__datas_alocado = []

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
    def is_concluida(self) -> bool:
        return self.__concluida_em is not None

    @property
    def concluida_em(self) -> datetime:
        return self.__concluida_em

    @concluida_em.setter
    def concluida_em(self, concluida_em: str):
        self.__concluida_em = concluida_em

    @property
    def tag(self) -> Tag:
        return self.__tag

    @tag.setter
    def tag(self, tag: Tag):
        self.__tag = tag

    @property
    def anotacoes(self) -> List[Anotacao]:
        return self.__anotacoes

    def add_anotacao(self, texto_anotacao: str):
        self.__anotacoes.push(Anotacao(texto_anotacao, self))

    def delete_anotacao(self, anotacao: Anotacao):
        if anotacao in self.__anotacoes:
            self.__anotacoes.remove(anotacao)
        else:
            raise NotFound()

    def add_data_alocado(self, dia, mes, ano):
        self.__datas_alocado.append([dia, mes, ano])

    def datas_alocado(self):
        return self.__datas_alocado
