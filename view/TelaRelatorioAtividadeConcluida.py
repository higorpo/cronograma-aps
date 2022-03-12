from view.AbstractTela import AbstractTela
import PySimpleGUI as sg


class TelaRelatorioAtividadeConcluida(AbstractTela):
    def __init__(self, controlador):
        sg.ChangeLookAndFeel('Reddit')

        super().__init__(controlador, nome_tela='Atividades concluídas')

    def init_components(self, data):
        headings = ['Código', 'Nome da atividade', 'Disciplina',
                    'Tag', 'Grau de dificuldade', 'Data de entrega', 'Concluída em']
        layout = super()\
            .layout_tela_lista(headings=headings, values=data, modulo_nome='atividade', btn_visualizar_enabled=False, btn_confirmar_enabled=False, btn_deletar_enabled=False, btn_cadastrar_enabled=False, btn_editar_enabled=False)  # TODO: Habilitar botão

        super().set_tela_layout(layout, size=(980, 680))

    def abrir_tela(self, data):
        self.init_components(data)

        while True:
            event, values = super().abrir_tela()

            # Quando fechar a tela
            if event == sg.WIN_CLOSED:
                return ('exited', None)
            if event == '-TABLE-' and len(values['-TABLE-']) != 0:
                pass
            else:
                return (event, values)
