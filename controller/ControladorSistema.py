import PySimpleGUI as sg
from controller.ControladorAtividade import ControladorAtividade
from controller.ControladorAtividadeDisciplina import ControladorAtividadeDisciplina
from controller.ControladorConcluirAtividade import ControladorConcluirAtividade
from controller.ControladorRelatorioAtividadeConcluida import ControladorRelatorioAtividadeConcluida
from controller.ControladorDisciplina import ControladorDisciplina
from controller.ControladorPeriodoLetivo import ControladorPeriodoLetivo
from controller.ControladorTag import ControladorTag
from controller.ControladorVisualizarCronograma import ControladorVisualizarCronograma
from view.TelaSistema import TelaSistema
from view.TelaMensagemSistema import TelaMensagemSistema
from messages.Sistema import mensagens_sistema


class ControladorSistema:
    __instance = None

    def __init__(self):
        self.__controlador_periodo_letivo = ControladorPeriodoLetivo(self)
        self.__controlador_disciplina = ControladorDisciplina(self)
        self.__controlador_tag = ControladorTag(self)
        self.__controlador_atividade = ControladorAtividade(self)
        self.__controlador_atividade_disciplina = ControladorAtividadeDisciplina(
            self
        )
        self.__controlador_visualizar_cronograma = ControladorVisualizarCronograma(
            self
        )
        self.__controlador_concluir_atividade = ControladorConcluirAtividade(
            self
        )
        self.__controlador_relatorio_atividade_concluida = ControladorRelatorioAtividadeConcluida(
            self
        )
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
            0: self.__controlador_visualizar_cronograma.abre_tela,
            1: self.__controlador_relatorio_atividade_concluida.abre_tela,
            2: self.__controlador_periodo_letivo.abre_tela,
            3: self.__controlador_disciplina.abre_tela,
            4: self.__controlador_atividade.abre_tela,
            5: None,
            6: self.__controlador_tag.abre_tela,
            7: self.fechar_sistema
        }

        while True:
            opcao_selecionada = self.__tela_sistema.abrir_tela([
                mensagens_sistema.get('menu_cronograma'),
                mensagens_sistema.get('menu_relatorio_atividade_concluida'),
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
        self.__controlador_atividade.dao.save_all()
        self.__controlador_atividade.cronograma_dao.save_all()
        self.__controlador_tag.dao.save_all()
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

    @property
    def controlador_atividade(self) -> ControladorAtividade:
        return self.__controlador_atividade

    @property
    def controlador_atividade_disciplina(self) -> ControladorAtividadeDisciplina:
        return self.__controlador_atividade_disciplina

    @property
    def controlador_relatorio_atividade_concluida(self) -> ControladorRelatorioAtividadeConcluida:
        return self.__controlador_relatorio_atividade_concluida

    @property
    def controlador_tag(self) -> ControladorTag:
        return self.__controlador_tag

    @property
    def controlador_visualizar_cronograma(self) -> ControladorVisualizarCronograma:
        return self.__controlador_visualizar_cronograma

    @property
    def controlador_concluir_atividade(self) -> ControladorConcluirAtividade:
        return self.__controlador_concluir_atividade
