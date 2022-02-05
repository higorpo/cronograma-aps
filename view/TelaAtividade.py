from view.AbstractTela import AbstractTela
import PySimpleGUI as sg


class TelaAtividade(AbstractTela):
    def __init__(self, controlador):
        sg.ChangeLookAndFeel('Reddit')

        super().__init__(controlador, nome_tela='Atividades')

    def init_components(self, data):
        headings = ['Código', 'Nome da atividade', 'Disciplina',
                    'Tag', 'Grau de dificuldade', 'Prazo de entrega', 'Tempo recomendado (em minutos)']
        layout = super()\
            .layout_tela_lista(headings=headings, values=data, modulo_nome='atividade', btn_visualizar_enabled=True)

        super().set_tela_layout(layout, size=(980, 680))

    def abrir_tela(self, data):
        self.init_components(data)

        while True:
            event, values = super().abrir_tela()

            # Quando fechar a tela
            if event == sg.WIN_CLOSED:
                return ('exited', None)
            if event == '-TABLE-' and len(values['-TABLE-']) != 0:
                column_editar_deletar = super()._window.FindElement(
                    'column_editar_deletar'
                )
                column_editar_deletar.Update(visible=True)
            elif (event == 'btn_editar' or event == 'btn_deletar' or event == 'btn_visualizar') and len(values['-TABLE-']) == 0:
                sg.popup_no_buttons(
                    'Você precisa selecionar um item da lista para\npoder realizar esta ação.',
                    title='Erro'
                )
            elif (event == 'btn_editar' or event == 'btn_deletar' or event == 'btn_visualizar') and len(values['-TABLE-']) != 0:
                return (event, data[values['-TABLE-'][0]][0])
            else:
                return (event, values)
