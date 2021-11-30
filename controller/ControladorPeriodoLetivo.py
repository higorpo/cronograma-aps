from dao.PeriodoLetivoDAO import PeriodoLetivoDAO
from messages.PeriodoLetivo import mensagens_periodo_letivo
from model.PeriodoLetivo import PeriodoLetivo
from utils.exceptions.TelaFechada import TelaFechada
from view.TelaPeriodoLetivo import TelaPeriodoLetivo
from view.TelaPeriodoLetivoCadastro import TelaPeriodoLetivoCadastro
from view.TelaPeriodoLetivoSelecao import TelaPeriodoLetivoSelecao


class ControladorPeriodoLetivo:
    __instance = None

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaPeriodoLetivo(self)
        self.__tela_cadastro = TelaPeriodoLetivoCadastro(self)
        self.__tela_selecao = TelaPeriodoLetivoSelecao(self)
        self.__dao = PeriodoLetivoDAO()

    def __new__(cls, _):
        if ControladorPeriodoLetivo.__instance is None:
            ControladorPeriodoLetivo.__instance = object.__new__(cls)
        return ControladorPeriodoLetivo.__instance

    @property
    def dao(self) -> PeriodoLetivoDAO:
        return self.__dao

    def abre_tela(self):
        while True:
            event, values = self.__tela.abrir_tela(self.map_object_to_array())
            if event == 'exited':
                break
            elif event == 'btn_cadastrar':
                self.__tela.fechar_tela()
                self.adicionar()
            elif event == 'btn_deletar':
                self.excluir(values)
                self.__tela.fechar_tela()
            elif event == 'btn_editar':
                self.__tela.fechar_tela()
                self.editar(values)
            elif event == 'btn_visualizar':
                self.__tela.fechar_tela()
                self.__controlador_sistema\
                    .mensagem_sistema.warning('Ainda não implementado!')

    def map_object_to_array(self):
        return list(map(lambda item: [item.id, item.nome], self.__dao.get_all()))

    def adicionar(self):
        event, dados_periodo_letivo = self.__tela_cadastro.abrir_tela(
            False, None)

        if event == 'criar':
            periodos_letivos = self.__dao.get_all()
            if len([x for x in periodos_letivos if x.nome == dados_periodo_letivo['nome']]) == 0:
                instancia_cliente = PeriodoLetivo(
                    *dados_periodo_letivo.values())

                self.__dao.add(instancia_cliente)
                return instancia_cliente
            else:
                self.__controlador_sistema\
                    .mensagem_sistema.warning(mensagens_periodo_letivo.get('ja_cadastrado'))

    def excluir(self, codigo_periodo_letivo):
        codigos_periodos_das_disciplinas = list(map(
            lambda x: x.periodo_letivo.id, self.__controlador_sistema.controlador_disciplina.disciplinas))
        try:
            if codigo_periodo_letivo in codigos_periodos_das_disciplinas:
                raise DelecaoCascataPeriodo
            else:
                periodo_letivo = self.__dao.get(codigo_periodo_letivo)
                self.__dao.remove(periodo_letivo)
        except Exception:
            self.__controlador_sistema\
                .mensagem_sistema.error(mensagens_periodo_letivo.get('erro_excluir'))

    def editar(self, codigo_periodo_letivo):
        periodo_letivo = self.__dao.get(codigo_periodo_letivo)

        event, dados_periodo_letivo = self.__tela_cadastro.abrir_tela(
            True, periodo_letivo)

        if event == 'exited':
            return
        elif event == 'criar':
            nome = dados_periodo_letivo.get('nome')
            periodo_letivo.nome = nome

    def buscar(self) -> PeriodoLetivo:
        event, key = self.__tela_selecao.abrir_tela(
            self.map_object_to_array()
        )

        if event == 'exited':
            raise TelaFechada
        elif event == 'selecionado':
            return self.__dao.get(key)

    @ property
    def periodo_letivos(self):
        return self.__dao.get_all()
