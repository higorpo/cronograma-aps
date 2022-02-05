from dao.AtividadeDAO import AtividadeDAO
from dao.CronogramaDAO import CronogramaDAO
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
        self.__cronograma_dao = CronogramaDAO()
        self.__disciplinas = controlador_sistema.controlador_disciplina.dao.get_all()
        self.__tags = controlador_sistema.controlador_tag.dao.get_all()

    def __new__(cls, _):
        if ControladorAtividade.__instance is None:
            ControladorAtividade.__instance = object.__new__(cls)
        return ControladorAtividade.__instance

    @property
    def dao(self) -> AtividadeDAO:
        return self.__dao

    @property
    def cronograma_dao(self) -> CronogramaDAO:
        return self.__cronograma_dao

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
        graus_dificuldade_tempo = {
            'fácil': 30, 'médio': 60, 'díficil': 90, 'muito difícil': 120
        }

        return list(map(lambda item: [item.id, item.nome, item.disciplina.nome, 'Sem tag' if item.tag is None else item.tag.nome, item.grau_dificuldade, item.prazo_entrega, graus_dificuldade_tempo[item.grau_dificuldade]], self.__dao.get_all()))

    def adicionar(self):
        event, dados_atividade = self.__tela_cadastro.abrir_tela(
            False, None, self.__disciplinas, self.__tags)

        if event == 'criar':
            atividades = self.__dao.get_all()
            if len([x for x in atividades if x.nome == dados_atividade['nome']]) == 0:
                disciplina_escolhida = [
                    x for x in self.__disciplinas if x.id == dados_atividade['disciplina']][0]

                instancia_atividade = Atividade(
                    dados_atividade['nome'], disciplina_escolhida, dados_atividade['grau_dificuldade'], dados_atividade['prazo_entrega'])

                tag_escolhida = None if dados_atividade['tag'] == None else [
                    x for x in self.__tags if x.id == dados_atividade['tag']][0]

                instancia_atividade.tag = tag_escolhida

                mensagem_retorno = self.__cronograma_dao.add_atividade(
                    instancia_atividade)

                if mensagem_retorno is not None:
                    self.__controlador_sistema.mensagem_sistema.info(
                        mensagem_retorno
                    )

                self.__dao.add(instancia_atividade)

                return instancia_atividade
            else:
                self.__controlador_sistema\
                    .mensagem_sistema.warning(mensagens_atividade.get('ja_cadastrado'))

    def excluir(self, codigo_atividade):
        try:
            atividade = self.__dao.get(codigo_atividade)
            self.__cronograma_dao.deleta_alocacao_atividade(atividade)
            self.__dao.remove(atividade)
        except Exception:
            self.__controlador_sistema\
                .mensagem_sistema.error(mensagens_atividade.get('erro_excluir'))

    def editar(self, codigo_atividade):
        atividade = self.__dao.get(codigo_atividade)

        event, dados_atividade = self.__tela_cadastro.abrir_tela(
            True, atividade, self.__disciplinas, self.__tags)

        if event == 'exited':
            return
        elif event == 'criar':
            nome = dados_atividade.get('nome')
            grau_dificuldade = dados_atividade.get('grau_dificuldade')
            prazo_entrega = dados_atividade.get('prazo_entrega')

            tag_escolhida = None if dados_atividade['tag'] == None else [
                x for x in self.__tags if x.id == dados_atividade['tag']][0]

            atividade.tag = tag_escolhida

            atividade.nome = nome
            atividade.grau_dificuldade = grau_dificuldade
            atividade.prazo_entrega = prazo_entrega

    @property
    def atividades(self):
        return self.__dao.get_all()
