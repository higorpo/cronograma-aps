import PySimpleGUI as sg
import datetime
from model.Atividade import Atividade
from utils.Validators import Validators
from utils.Formatters import Formatters
from view.AbstractTela import AbstractTela
from messages.Atividade import mensagens_atividade


class TelaAtividadeCadastro(AbstractTela):
    def __init__(self, controlador):
        sg.ChangeLookAndFeel('Reddit')

        super().__init__(controlador, nome_tela='Atividade')

    def init_components(self, modo_edicao, data: Atividade, disciplinas: list):
        layout = super().layout_tela_cadastro([
            {
                'key': 'nome_atividade',
                'label': mensagens_atividade.get('label_nome'),
                'type': 'text',
                'default_text': '' if modo_edicao == False else data.nome,
                'disabled': False
            },
            {
                'key': 'selecao_disciplina',
                'label': mensagens_atividade.get('label_nome_disciplina'),
                'type': 'combo',
                'default_value': '' if modo_edicao == False else data.disciplina.nome,
                'values': [x.nome for x in disciplinas],
                'disabled': modo_edicao
            },
            {
                'key': 'selecao_grau_dificuldade',
                'label': mensagens_atividade.get('label_grau'),
                'type': 'combo',
                'default_value': '' if modo_edicao == False else data.grau_dificuldade,
                'values': ['fácil', 'médio', 'díficil', 'muito difícil'],
                'disabled': modo_edicao  # Desabilita edição do campo se estiver editando uma atividade
            },
            {
                'key': 'selecao_tag',
                'label': mensagens_atividade.get('label_tag'),
                'type': 'combo',
                'default_value': '' if modo_edicao == False else 'Sem tag' if data.tag is None else data.tag.nome,
                'values': ['Sem tag'],
                'disabled': True  # Desabilita edição do campo se estiver editando uma atividade
            },
            {
                'key': 'prazo_de_entrega',
                'label': mensagens_atividade.get('label_prazo'),
                'type': 'text',
                'default_text': '' if modo_edicao == False else data.prazo_entrega,
                # Desabilita edição do prazo de entrega se estiver editando uma atividade
                'disabled': modo_edicao
            },
        ], modo_edicao)

        super().set_tela_layout(layout, size=(300, 400))

    def abrir_tela(self, modo_edicao, data: Atividade, disciplinas: list):
        self.init_components(modo_edicao, data, disciplinas)

        # Armazena para cada um dos inputs se ele está válido ou não.
        valido = [modo_edicao] * 4

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
                    'Atividade deve ter entre 3 a 30 caracteres.'  # Verificar regras de negócio
                )
                continue
            elif event == 'input_selecao_disciplina':
                valido[1] = super().validar_input(
                    event,
                    values['input_selecao_disciplina'] == '',
                    'É preciso selecionar uma disciplina'
                )
                continue
            elif event == 'input_selecao_grau_dificuldade':
                valido[2] = super().validar_input(
                    event,
                    values['input_selecao_grau_dificuldade'] not in [
                        'fácil', 'médio', 'díficil', 'muito difícil'],
                    'É preciso selecionar um grau de dificuldade'
                )
                continue
            elif event == 'input_prazo_de_entrega':
                valido_prazo_entrega = [False, False, False]

                valido_prazo_entrega[0] = super().validar_input(
                    event,
                    not Validators.validar_data(
                        values['input_prazo_de_entrega']),
                    'É preciso digitar uma data válida no formato dia/mês/ano'
                )

                if valido_prazo_entrega[0] is True:
                    valido_prazo_entrega[1] = super().validar_input(
                        event,
                        not Validators.validar_data_reatrotiva(
                            values['input_prazo_de_entrega']),
                        'É preciso uma data maior que a data atual'
                    )

                if valido_prazo_entrega[1] is True:
                    valido_prazo_entrega[2] = super().validar_input(
                        event,
                        not Validators.validar_data_min_3_days(
                            values['input_prazo_de_entrega']),
                        'É preciso cadastrar no mínimo 3 dias antes'
                    )

                valido[3] = valido_prazo_entrega[2]
                continue
            elif event == 'btn_salvar':
                # Verifica se todos os campos são válidos, se não forem, exibe mensagem de erro.
                if False in valido:
                    sg.popup_no_buttons(
                        'Existem campos inválidos, corrija-os antes de salvar.',
                        title='Erro'
                    )
                else:
                    # Verifica se o valor do combo está certo...
                    super().fechar_tela()
                    disciplina_escolhida = [
                        x.id for x in disciplinas if x.nome == values['input_selecao_disciplina']][0]

                    return (
                        'criar', {
                            'nome': values['input_nome_atividade'],
                            'disciplina': disciplina_escolhida,
                            'grau_dificuldade': values['input_selecao_grau_dificuldade'],
                            'prazo_entrega': datetime.datetime.strptime(values['input_prazo_de_entrega'], "%d/%m/%Y")
                        }
                    )
            else:
                return (event, values)
