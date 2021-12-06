from dao.AtividadeDAO import AtividadeDAO
from messages.Atividade import mensagens_atividade
from model.Atividade import Atividade
from utils.exceptions.TelaFechada import TelaFechada
from view.TelaAtividade import TelaAtividade
from view.TelaAtividadeCadastro import TelaAtividadeCadastro


class ControladorAtividade:
    __instance = None

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaAtividade(self)
        self.__tela_cadastro = TelaAtividadeCadastro(self)
        self.__dao = AtividadeDAO()
        self.__atividade = controlador_sistema.controlador_atividade.dao.get_all()

    def __new__(cls, _):
        if ControladorAtividade.__instance is None:
            ControladorAtividade.__instance = object.__new__(cls)
        return ControladorAtividade.__instance

    @property
    def dao(self) -> AtividadeDAO:
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
        return list(map(lambda item: [item.id, item.nome, item.grau_dificuldade.nome, item.pra_entrega], self.__dao.get_all()))

    def adicionar(self):
        event, dados_atividade = self.__tela_cadastro.abrir_tela(
            False, None, self.__disciplina)

        if event == 'criar':
            atividade = self.__dao.get_all()
            if len([x for x in atividade if x.nome == dados_atividade['nome']]) == 0:
                disciplina_escolhida = [
                    x for x in self.__disciplina if x.id == dados_atividade['disciplina']][0]
                instancia_atividade = Atividade(
                    dados_atividade['nome'], disciplina_escolhida)

                self.__dao.add(instancia_atividade)
                return instancia_atividade
            else:
                self.__controlador_sistema\
                    .mensagem_sistema.warning(mensagens_atividade.get('ja_cadastrado'))

    def excluir(self, codigo_atividade):
        try:
            atividade = self.__dao.get(codigo_atividade)
            self.__dao.remove(atividade)
        except Exception:
            self.__controlador_sistema\
                .mensagem_sistema.error(mensagens_atividade.get('erro_excluir'))

    def editar(self, codigo_atividade):
        atividade = self.__dao.get(codigo_atividade)

        event, dados_atividade = self.__tela_cadastro.abrir_tela(
            True, atividade, self.__disciplina)

        if event == 'exited':
            return
        elif event == 'criar':
            nome = dados_atividade.get('nome')
            disciplina = [
                x for x in self.__atividade if x.id == dados_atividade.get('disciplina')][0]
            atividade.nome = nome
            atividade.disciplina = disciplina

    def buscar(self) -> Atividade:
        event, key = self.__tela_selecao.abrir_tela(
            self.map_object_to_array()
        )

        if event == 'exited':
            raise TelaFechada
        elif event == 'selecionado':
            return self.__dao.get(key)

    @property
    def atividade(self):
        return self.__dao.get_all()
