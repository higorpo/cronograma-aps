from dao.AtividadeDAO import AtividadeDAO
from dao.CronogramaDAO import CronogramaDAO
from view.TelaRelatorioAtividadeConcluida import TelaRelatorioAtividadeConcluida


class ControladorRelatorioAtividadeConcluida:
    __instance = None

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaRelatorioAtividadeConcluida(self)

    def __new__(cls, _):
        if ControladorRelatorioAtividadeConcluida.__instance is None:
            ControladorRelatorioAtividadeConcluida.__instance = object.__new__(
                cls
            )
        return ControladorRelatorioAtividadeConcluida.__instance

    @property
    def dao(self) -> AtividadeDAO:
        return self.__controlador_sistema.controlador_atividade.dao

    def abre_tela(self):
        self.__tela.abrir_tela(self.map_object_to_array())

    def map_object_to_array(self):
        return list(map(lambda item: [item.id, item.nome, item.disciplina.nome, 'Sem tag' if item.tag is None else item.tag.nome, item.grau_dificuldade, item.prazo_entrega, item.concluida_em], self.dao.get_atividades_concluidas()))
