import PySimpleGUI as sg
from model.Atividade import Atividade
from utils.Validators import Validators
from utils.Formatters import Formatters
from view.AbstractTela import AbstractTela
from messages.Atividade import mensagens_atividade


class TelaAtividadeCadastro(AbstractTela):
    def __init__(self, controlador):
        sg.ChangeLookAndFeel('Reddit')

        super().__init__(controlador, nome_tela='Atividade')

    def init_components(self, modo_edicao, data: Atividade, disciplina: list, tag, grau_de_dificuldade, prazo_entrega):
        layout = super().layout_tela_cadastro([
            {
                'key': 'nome_atividade',
                'label': mensagens_atividade.get('label_nome'),
                'type': 'text',
                'default_text': '' if modo_edicao == False else data.nome,
                'disabled': False
            },
            {
                'key': 'nome_disciplina',
                'label': mensagens_atividade.get('label_nome_disciplina'),
                'type': 'text',
                'default_text': '' if modo_edicao == False else data.nome,
                'disabled': False
            },
            {
                'key': 'grau_de_dificuldade',
                'label': mensagens_atividade.get('label_grau'),
                'type': 'text',
                'default_text': '' if modo_edicao == False else data.nome,
                'disabled': False
            },
            {
                'key': 'prazo_de_entrega',
                'label': mensagens_atividade.get('label_prazo'),
                'type': 'text',
                'default_text': '' if modo_edicao == False else data.nome,
                'disabled': False
            },
        ], modo_edicao)

        super().set_tela_layout(layout, size=(300, 400))

    def abrir_tela(self, modo_edicao, data: Atividade, disciplina: list, tag, grau_de_dificuldade, prazo_entrega):
        self.init_components(modo_edicao, data, disciplina, tag, grau_de_dificuldade, prazo_entrega)

        # Armazena para cada um dos inputs se ele está válido ou não.
        valido = [modo_edicao] * 5

        while True:
            event, values = super().abrir_tela()

            # Caso o usuário feche a janela do programa
            if event == sg.WIN_CLOSED:
                return ('exited', None)

            # Valida os inputs de texto
            elif event == 'input_nome_atividade':
                valido[0] = super().validar_input(
                    event,
                    len(values[event]) < 3 or len(values[event]) > 30,
                    'Atividade deve ter entre 3 a 30 caracteres.'
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
            else:
                return (event, values)
