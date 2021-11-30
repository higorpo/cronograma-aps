import PySimpleGUI as sg
from controller.ControladorDisciplina import ControladorDisciplina
from controller.ControladorPeriodoLetivo import ControladorPeriodoLetivo
from view.TelaSistema import TelaSistema
from view.TelaMensagemSistema import TelaMensagemSistema
from messages.Sistema import mensagens_sistema


class ControladorSistema:
    __instance = None

    def __init__(self):
        self.__controlador_periodo_letivo = ControladorPeriodoLetivo(self)
        self.__controlador_disciplina = ControladorDisciplina(self)
        self.__tela_sistema = TelaSistema(self)
        self.__tela_mensagem_sistema = TelaMensagemSistema(self)

    def __new__(cls):
        if ControladorSistema.__instance is None:
            ControladorSistema.__instance = object.__new__(cls)
        return ControladorSistema.__instance

    def inicializa_sistema(self):
        try:
            self.abre_tela()
        except NotImplementedError:
            exit(0)

    def abre_tela(self):
        lista_opcoes = {
            0: None,
            1: self.__controlador_periodo_letivo.abre_tela,
            2: self.__controlador_disciplina.abre_tela,
            3: None,
            4: None,
            5: None,
            7: self.fechar_sistema
        }

        while True:
            opcao_selecionada = self.__tela_sistema.abrir_tela([
                mensagens_sistema.get('menu_cronograma'),
                mensagens_sistema.get('menu_periodos_letivos'),
                mensagens_sistema.get('menu_disciplinas'),
                mensagens_sistema.get('menu_atividades'),
                mensagens_sistema.get('menu_anotacoes'),
                mensagens_sistema.get('menu_tags'),
                mensagens_sistema.get('menu_sair_sistema')
            ])

            try:
                self.__tela_sistema.fechar_tela()

                if opcao_selecionada == sg.WIN_CLOSED:
                    self.fechar_sistema()
                    return

                lista_opcoes[opcao_selecionada]()

            except KeyError:
                raise NotImplementedError

    def fechar_sistema(self):
        self.__controlador_periodo_letivo.dao.save_all()
        self.__controlador_disciplina.dao.save_all()
        exit(0)

    @property
    def mensagem_sistema(self) -> TelaMensagemSistema:
        return self.__tela_mensagem_sistema

    @property
    def controlador_periodo_letivo(self) -> ControladorPeriodoLetivo:
        return self.__controlador_periodo_letivo

    @property
    def controlador_disciplina(self) -> ControladorDisciplina:
        return self.__controlador_disciplina
