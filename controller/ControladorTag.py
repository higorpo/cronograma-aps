from dao.TagDAO import TagDAO
from messages.Tag import mensagens_tag
from model.Tag import Tag
from utils.exceptions.TelaFechada import TelaFechada
from view.TelaTag import TelaTag
from view.TelaTagCadastro import TelaTagCadastro


class ControladorTag:
    __instance = None

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaTag(self)
        self.__tela_cadastro = TelaTagCadastro(self)
        self.__dao = TagDAO()

    def __new__(cls, _):
        if ControladorTag.__instance is None:
            ControladorTag.__instance = object.__new__(cls)
        return ControladorTag.__instance

    @property
    def dao(self) -> TagDAO:
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
        event, dados_tag = self.__tela_cadastro.abrir_tela(False, None)

        if event == 'criar':
            tags = self.__dao.get_all()
            if len([x for x in tags if x.nome == dados_tag['nome']]) == 0:
                instancia_cliente = Tag(*dados_tag.values())

                self.__dao.add(instancia_cliente)
                return instancia_cliente
            else:
                self.__controlador_sistema\
                    .mensagem_sistema.warning(mensagens_tag.get('ja_cadastrado'))

    def excluir(self, codigo_tag):
        print(codigo_tag)
        codigos_tags_das_disciplinas = list(map(
            lambda x: x.tag and x.tag.id, self.__controlador_sistema.controlador_atividade.atividades))

        try:
            if codigo_tag in codigos_tags_das_disciplinas:
                self.__controlador_sistema\
                    .mensagem_sistema.error(mensagens_tag.get('erro_tag_com_atividade'))
            else:
                tag = self.__dao.get(codigo_tag)
                self.__dao.remove(tag)
        except Exception:
            self.__controlador_sistema\
                .mensagem_sistema.error(mensagens_tag.get('erro_excluir'))

    def editar(self, codigo_tag):
        tag = self.__dao.get(codigo_tag)

        event, dados_tag = self.__tela_cadastro.abrir_tela(True, tag)

        if event == 'exited':
            return
        elif event == 'criar':
            nome = dados_tag.get('nome')
            tag.nome = nome

    @ property
    def tags(self):
        return self.__dao.get_all()
