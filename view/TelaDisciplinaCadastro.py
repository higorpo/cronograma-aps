import PySimpleGUI as sg
from model.Disciplina import Disciplina
from utils.Validators import Validators
from utils.Formatters import Formatters
from view.AbstractTela import AbstractTela
from messages.Disciplina import mensagens_disciplina


class TelaDisciplinaCadastro(AbstractTela):
    def __init__(self, controlador):
        sg.ChangeLookAndFeel('Reddit')

        super().__init__(controlador, nome_tela='Disciplina')

    def init_components(self, modo_edicao, data: Disciplina, periodos_letivos: list):
        layout = super().layout_tela_cadastro([
            {
                'key': 'nome_disciplina',
                'label': mensagens_disciplina.get('label_nome'),
                'type': 'text',
                'default_text': '' if modo_edicao == False else data.nome,
                'disabled': False
            },
            {
                'key': 'selecao_periodo_letivo',
                'label': mensagens_disciplina.get('selecionar_periodo_letivo'),
                'type': 'combo',
                'default_value': '' if modo_edicao == False else data.periodo_letivo.nome,
                'values': [x.nome for x in periodos_letivos],
                'disabled': False
            },
        ], modo_edicao)

        super().set_tela_layout(layout, size=(300, 400))

    def abrir_tela(self, modo_edicao, data: Disciplina, periodos_letivos: list):
        self.init_components(modo_edicao, data, periodos_letivos)

        # Armazena para cada um dos inputs se ele está válido ou não.
        valido = [modo_edicao] * 2

        while True:
            event, values = super().abrir_tela()

            # Caso o usuário feche a janela do programa
            if event == sg.WIN_CLOSED:
                return ('exited', None)

            # Valida os inputs de texto
            elif event == 'input_nome_disciplina':
                valido[0] = super().validar_input(
                    event,
                    len(values[event]) < 3 or len(values[event]) > 10,
                    'Disciplina deve ter entre 3 a 10 caracteres.'
                )
                continue
            elif event == 'input_selecao_periodo_letivo':
                valido[1] = super().validar_input(
                    event,
                    values['input_selecao_periodo_letivo'] == '',
                    'É preciso selecionar uma disciplina'
                )
                continue
            elif event == 'btn_salvar':
                # Verifica se todos os campos são válidos, se não forem, exibe mensagem de erro.
                if False in valido:
                    sg.popup_no_buttons(
                        'Existem campos inválidos, corrija-os antes de salvar.',
                        title='Erro'
                    )
                    continue
                else:
                    # Verifica se o valor do combo está certo...
                    super().fechar_tela()
                    periodo_letivo_escolhido = [
                        x.id for x in periodos_letivos if x.nome == values['input_selecao_periodo_letivo']][0]
                    return (
                        'criar', {
                            'nome': values['input_nome_disciplina'],
                            'periodo_letivo': periodo_letivo_escolhido
                        }
                    )
            else:
                return (event, values)
