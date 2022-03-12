from dao.AtividadeDAO import AtividadeDAO
from view.TelaAtividadeDisciplina import TelaAtividadeDisciplina


class ControladorAtividadeDisciplina:
    __instance = None

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaAtividadeDisciplina(self)

    def __new__(cls, _):
        if ControladorAtividadeDisciplina.__instance is None:
            ControladorAtividadeDisciplina.__instance = object.__new__(cls)
        return ControladorAtividadeDisciplina.__instance

    @property
    def dao(self) -> AtividadeDAO:
        return self.__controlador_sistema.controlador_atividade.dao

    def abre_tela(self, codigo_disciplina):
        self.__tela.abrir_tela(self.map_object_to_array(codigo_disciplina))

    def map_object_to_array(self, codigo_disciplina):
        graus_dificuldade_tempo = {
            'fácil': 30, 'médio': 60, 'díficil': 90, 'muito difícil': 120
        }

        return list(map(lambda item: [item.id, item.nome, item.disciplina.nome, 'Sem tag' if item.tag is None else item.tag.nome, item.grau_dificuldade, item.prazo_entrega, graus_dificuldade_tempo[item.grau_dificuldade]], self.dao.get_all_by_disciplina(codigo_disciplina)))
