import PySimpleGUI as sg
from model.Tag import Tag
from view.AbstractTela import AbstractTela
from messages.Tag import mensagens_tag


class TelaTagCadastro(AbstractTela):
    def __init__(self, controlador):
        sg.ChangeLookAndFeel('Reddit')

        super().__init__(controlador, nome_tela='Tags')

    def init_components(self, modo_edicao, data: Tag):
        layout = super().layout_tela_cadastro([
            {
                'key': 'nome_tag',
                'label': mensagens_tag.get('label_nome'),
                'type': 'text',
                'default_text': '' if modo_edicao == False else data.nome,
                'disabled': False
            },
        ], modo_edicao)

        super().set_tela_layout(layout, size=(300, 400))

    def abrir_tela(self, modo_edicao, data: Tag):
        self.init_components(modo_edicao, data)

        # Armazena para cada um dos inputs se ele está válido ou não.
        valido = [modo_edicao] * 1

        while True:
            event, values = super().abrir_tela()

            # Caso o usuário feche a janela do programa
            if event == sg.WIN_CLOSED:
                return ('exited', None)

            # Valida os inputs de texto
            elif event == 'input_nome_tag':
                valido[0] = super().validar_input(
                    event,
                    len(values[event]) < 3 or len(values[event]) > 20,
                    'A tag deve ter entre 3 a 20 caracteres.'
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
                    return (
                        'criar', {
                            'nome': values['input_nome_tag'],
                        }
                    )
            else:
                return (event, values)
