from dao.AtividadeDAO import AtividadeDAO
from model.Atividade import Atividade
from view.TelaConcluirAtividade import TelaConcluirAtividade
from datetime import datetime, timedelta


class ControladorConcluirAtividade:
    __instance = None

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaConcluirAtividade(self)
        self.__atividade_dao = AtividadeDAO()

    def __new__(cls, _):
        if ControladorConcluirAtividade.__instance is None:
            ControladorConcluirAtividade.__instance = object.__new__(cls)
        return ControladorConcluirAtividade.__instance

    @property
    def atividade_dao(self) -> AtividadeDAO:
        return self.__atividade_dao

    def abre_tela(self, atividade: Atividade):
        while True:
            event, values = self.__tela.abrir_tela(atividade)
            if event == 'exited':
                break
            elif event == 'btn_salvar':
                self.__tela.fechar_tela()
                self.concluir(values["marcou_concluida"], atividade)
                break

    def concluir(self, marcou_concluida: bool, atividade: Atividade):
        if marcou_concluida:
            atividade.concluida_em = datetime.today().strftime("%d/%m/%Y")
            self.__atividade_dao.remove(atividade)
            self.__atividade_dao.add(atividade)
