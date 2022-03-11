import PySimpleGUI as sg
from dao.AtividadeDAO import AtividadeDAO
from view.AbstractTela import AbstractTela
from model.Atividade import Atividade
from messages.Atividade import mensagens_atividade


class TelaConcluirAtividade(AbstractTela):
    def __init__(self, controlador):
        sg.ChangeLookAndFeel('Reddit')

        super().__init__(controlador, nome_tela='Concluir atividade')

    def init_components(self, data: Atividade):
        layout = super().layout_tela_cadastro([
            {
                'text': mensagens_atividade.get('label_conclusao_checkbox'),
                'key': 'concluir_atividade',
                'label': mensagens_atividade.get('concluir')(data.nome),
                'type': 'checkbox',
                'disabled': False
            },
        ])

        super().set_tela_layout(layout, size=(300, 400))

    def abrir_tela(self, data: Atividade):
        self.init_components(data)

        while True:
            event, values = super().abrir_tela()
            if event == sg.WIN_CLOSED:
                return ('exited', None)
            elif event == 'input_concluir_atividade':
                continue
            elif event == 'btn_salvar':
                super().fechar_tela()
                return (
                    'btn_salvar', {
                        'marcou_concluida': values['input_concluir_atividade'],
                    }
                )
            else:
                return (event, values)
