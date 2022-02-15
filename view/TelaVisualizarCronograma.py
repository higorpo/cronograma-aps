from operator import index
from turtle import color
from model.Atividade import Atividade
from model.Tag import Tag
from view.AbstractTela import AbstractTela
import PySimpleGUI as sg


k_card_color = '#f7f7f7'
k_tag_color = '#c9c9c9'


class TelaVisualizarCronograma(AbstractTela):
    def __init__(self, controlador):
        sg.ChangeLookAndFeel('Reddit')

        super().__init__(controlador, nome_tela='VisualizarCronograma')

    def init_components(self, data):

        dias_da_semana_texto = ['Segunda-feira', 'Terça-feira',
                                'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']

        def atividades_do_dia(atividades: list):
            return list(map(lambda atividade: [atividade_card(
                atividade['nome'], atividade['prazo_entrega'], atividade['tag'], atividade['id'], atividade['tempo'])], atividades))

        def dia_semana_tile(index: int):
            atividades = data['atividades'][index]
            dia_da_semana_numero = data['dias_semana'][index]
            return sg.Column([
                [sg.Text(f"{dias_da_semana_texto[index]}, {dia_da_semana_numero}", font=(
                    '', 12, 'bold'))],
                [sg.Column(atividades_do_dia(atividades))] if len(atividades) != 0 else [
                    sg.Text('Nenhuma atividade alocada ainda...')]
            ]
            )

        def atividade_card(nome: str, prazo_entrega: str, tag: Tag, id: str, tempo: int):
            return sg.Frame(title='', layout=[[
                sg.Column([
                    [
                          sg.Text(text=nome,
                                  background_color=k_card_color,
                                  font=('', 16, 'normal'),
                                  ),
                          ],
                    [
                        sg.Text(text=f'Tag: {tag}',
                                background_color=k_tag_color),
                        sg.Text(text=f'Prazo: {prazo_entrega}',
                                background_color=k_tag_color),
                        sg.Text(text=f'Tempo: {30 * tempo}min',
                                background_color=k_tag_color),
                    ],
                ], size=(400, 100), background_color=k_card_color),
                sg.Column([
                    [sg.Text('Criar nota', key=f'criar_{id}', text_color='#37a0fc', font=('', 10, 'bold'),
                             enable_events=True, background_color=k_card_color)],
                    [sg.Text('Concluir', key=f'concluir_{id}', text_color='#37a0fc', font=('', 10, 'bold'),
                             enable_events=True, background_color=k_card_color)],
                    [sg.Text('Excluir', key=f'excluir_{id}', text_color='#37a0fc', font=('', 10, 'bold'),
                             enable_events=True, background_color=k_card_color)],
                ], size=(100, 100), element_justification='right', background_color=k_card_color),
            ]], size=(500, 100), background_color=k_card_color)

        def callable(size):
            dias_cronograma = []
            for i in range(7):
                dias_cronograma.append([dia_semana_tile(i)])

            return [[
                sg.Column(scrollable=True,
                          vertical_scroll_only=True,
                          size=(600, 1000),
                          element_justification='left',
                          vertical_alignment='center',
                          justification='center',
                          layout=dias_cronograma)
            ]]

        layout = callable

        # Define o tamanho do layout
        super().set_tela_layout(layout, size=(980, 680))

    def abrir_tela(self, data):
        self.init_components(data)

        while True:
            event, values = super().abrir_tela()

            # Quando fechar a tela
            if event == sg.WIN_CLOSED:
                return ('exited', None)
            elif 'criar_' in event:
                sg.popup_no_buttons(
                    'Ainda não implementado!',
                    title='Erro'
                )
            elif 'concluir_' in event:
                sg.popup_no_buttons(
                    'Ainda não implementado!',
                    title='Erro'
                )
            elif 'excluir_' in event:
                escolha, _ = sg.Window('Atenção!', [[sg.T('Isso irá excluir todos blocos alocados para esta atividade. Deseja continuar?')], [
                    sg.Yes(s=10, button_text='Sim'), sg.No(s=10, button_text='Não')]], disable_close=True, modal=True).read(close=True)

                if escolha == 'Sim':
                    _, id_atividade_excluida = event.split('_')
                    return (event, id_atividade_excluida)
            else:
                return (event, values)
