import PySimpleGUI as sg
from messages.Sistema import mensagens_sistema
from view.AbstractTela import AbstractTela


class TelaSistema(AbstractTela):
    def __init__(self, controlador):
        sg.ChangeLookAndFeel('Reddit')

        super().__init__(controlador)

        self.__window = None

    def init_components(self, opcoes):
        lista_botoes = map(lambda x: [sg.Button(x[1], key=x[0], button_color='#52b1eb' if mensagens_sistema.get(
            'menu_sair_sistema') != x[1] else '#f03737', auto_size_button=False, size=(30, 2))], enumerate(opcoes))

        layout = [
            [sg.Text(mensagens_sistema.get('titulo_tela_opcoes_modulo')), ],
            lista_botoes
        ]
        w, h = sg.Window.get_screen_size()
        self.__window = sg.Window(
            'Cronograma semanal',
            location=(w/4 - 100, h/4),
        ).Layout(layout)

    def abrir_tela(self, opcoes=[]):
        self.init_components(opcoes)

        event, values = self.__window.Read()
        return event

    def fechar_tela(self):
        self.__window.close()
