from dao.DisciplinaDAO import DisciplinaDAO
from messages.Disciplina import mensagens_disciplina
from model.Disciplina import Disciplina
from utils.exceptions.TelaFechada import TelaFechada
from view.TelaDisciplina import TelaDisciplina
from view.TelaDisciplinaCadastro import TelaDisciplinaCadastro


class ControladorDisciplina:
    __instance = None

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaDisciplina(self)
        self.__tela_cadastro = TelaDisciplinaCadastro(self)
        self.__dao = DisciplinaDAO()
        self.__periodos_letivos = controlador_sistema.controlador_periodo_letivo.dao.get_all()

    def __new__(cls, _):
        if ControladorDisciplina.__instance is None:
            ControladorDisciplina.__instance = object.__new__(cls)
        return ControladorDisciplina.__instance

    @property
    def dao(self) -> DisciplinaDAO:
        return self.__dao

    def abre_tela(self):
        while True:
            event, values = self.__tela.abrir_tela(
                self.__map_object_to_array()
            )
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
                self.__controlador_sistema.controlador_atividade_disciplina.abre_tela(
                    values  # Código disciplina
                )

    def __map_object_to_array(self):
        return list(map(lambda item: [item.id, item.nome, item.periodo_letivo.nome], self.__dao.get_all()))

    def adicionar(self):
        event, dados_disciplina = self.__tela_cadastro.abrir_tela(
            False, None, self.__periodos_letivos)

        if event == 'criar':
            disciplinas = self.__dao.get_all()
            if len([x for x in disciplinas if x.nome == dados_disciplina['nome']]) == 0:
                periodo_letivo_escolhido = [
                    x for x in self.__periodos_letivos if x.id == dados_disciplina['periodo_letivo']][0]
                instancia_disciplina = Disciplina(
                    dados_disciplina['nome'], periodo_letivo_escolhido)

                self.__dao.add(instancia_disciplina)
                return instancia_disciplina
            else:
                self.__controlador_sistema\
                    .mensagem_sistema.warning(mensagens_disciplina.get('ja_cadastrado'))

    def excluir(self, codigo_disciplina):
        codigos_disciplinas_atividades = list(map(
            lambda x: x.disciplina.id, self.__controlador_sistema.controlador_atividade.atividades))

        try:
            if codigo_disciplina in codigos_disciplinas_atividades:
                self.__controlador_sistema\
                    .mensagem_sistema.error(mensagens_disciplina.get('erro_disciplina_com_atividade'))
            else:
                disciplina = self.__dao.get(codigo_disciplina)
                self.__dao.remove(disciplina)
        except Exception:
            self.__controlador_sistema\
                .mensagem_sistema.error(mensagens_disciplina.get('erro_excluir'))

    def editar(self, codigo_disciplina):
        disciplina = self.__dao.get(codigo_disciplina)

        event, dados_disciplina = self.__tela_cadastro.abrir_tela(
            True, disciplina, self.__periodos_letivos)

        if event == 'exited':
            return
        elif event == 'criar':
            nome = dados_disciplina.get('nome')
            periodo_letivo = [
                x for x in self.__periodos_letivos if x.id == dados_disciplina.get('periodo_letivo')][0]
            disciplina.nome = nome
            disciplina.periodo_letivo = periodo_letivo

    @property
    def disciplinas(self):
        return self.__dao.get_all()
