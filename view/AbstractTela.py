import re
import PySimpleGUI as sg
from abc import ABC, abstractmethod
from utils.exceptions.LayoutNotDefined import LayoutNotDefined
from utils.Validators import Validators
from utils.Formatters import Formatters


class AbstractTela(ABC):
    @abstractmethod
    def __init__(self, controlador, nome_tela=''):
        self.__controlador = controlador
        self.__nome_tela = nome_tela
        self.__window = None

        self.__table_key = None
        self.__layout_tabela = False

    @property
    def _controlador(self):
        return self.__controlador

    @property
    def _window(self):
        return self.__window

    def abrir_tela(self):
        return self.__window.Read()

    def fechar_tela(self):
        self._window.close()

    def set_tela_layout(self, layout, size=(780, 680)):
        if layout == None:
            raise LayoutNotDefined

        w, h = sg.Window.get_screen_size()
        self.__window = sg.Window(
            self.__nome_tela,
            size=size,
            location=(w/4 - (size[0]/2), h/4)
        ).Layout(layout(size))

    def layout_tela_cadastro(self, inputs, modo_edicao: bool = False):
        def map_inputs(input):
            inputElement = None

            if input['type'] == 'combo':
                inputElement = sg.Combo(
                    input['values'],
                    key='input_' + input['key'],
                    default_value=input['default_value'] if 'default_value' in input else '',
                    size=(21, 8),
                    font=('Arial', 15),
                    enable_events=True,
                    background_color='#ffffff',
                    disabled=input['disabled'] if 'disabled' in input else False
                )
            elif input['type'] == 'text':
                inputElement = sg.Input(
                    key='input_' + input['key'],
                    default_text=input['default_text'] if 'default_text' in input else '',
                    background_color='#ffffff',
                    font=('Arial', 15),
                    size=(22, 2),
                    enable_events=True,
                    disabled=input['disabled'] if 'disabled' in input else False
                )
            elif input['type'] == 'checkbox':
                inputElement = sg.Checkbox(
                    input['text'],
                    key='input_' + input['key'],
                    default=False,
                    size=(21, 8),
                    font=('Arial', 12),
                    enable_events=True,
                    background_color='#ffffff',
                    disabled=input['disabled'] if 'disabled' in input else False
                )

            return [
                sg.Column([
                    [
                        sg.Text(input['label'])
                    ],
                    [
                        inputElement
                    ],
                    [
                        sg.Text(
                            'Preencha este campo.' if modo_edicao == False else '',
                            key='input_' + input['key'] + '_hint',
                            font=('Arial', 8),
                            text_color='#ff0000',
                            visible=True,
                            auto_size_text=True,
                            size=(40, 1)
                        )
                    ]
                ])
            ]

        lista_inputs = list(map(map_inputs, inputs))

        lista_inputs.append([
            sg.Button(
                'Salvar',
                key='btn_salvar',
                size=(32, 2)
            )
        ])

        def callable(size):
            size_height = 150*len(lista_inputs) + 100
            size = (size[0], size_height)

            return [
                [
                    sg.Column(
                        lista_inputs,
                        size=size,
                        pad=(0, 0),
                        scrollable=True, vertical_scroll_only=True
                    )
                ]
            ]

        return callable

    def layout_tela_lista(self, headings=[], values=[], key='-TABLE-', modulo_nome='', btn_visualizar_enabled=False, btn_cadastrar_enabled=True, btn_deletar_enabled=True, btn_editar_enabled=True, btn_confirmar_enabled=False):
        self.__table_key = key
        self.__layout_tabela = True

        buttons = []

        visible_column_map = list(
            map(lambda value: value != 'Código', headings)
        )

        if btn_deletar_enabled:
            buttons.append(sg.Button(
                f'Deletar {modulo_nome}',
                key='btn_deletar',
                button_color='#e32f2f',
                size=(18, 2)
            ))

        if btn_editar_enabled:
            buttons.append(sg.Button(
                f'Editar {modulo_nome}',
                key='btn_editar',
                button_color='#000000',
                size=(18, 2)
            ))

        if btn_confirmar_enabled:
            buttons.append(sg.Button(
                f'Confirmar seleção',
                key='btn_confirmar',
                button_color='#e3a540',
                size=(18, 2)
            ))

        if btn_visualizar_enabled:
            buttons.append(sg.Button(
                f'Visualizar',
                key='btn_visualizar',
                button_color='#1aab3d',
                size=(18, 2)
            ))

        def callable(size):
            if len(values) > 0:
                tableElement = sg.Table(
                    values=values,
                    headings=headings,
                    display_row_numbers=True,
                    visible_column_map=visible_column_map,
                    enable_events=True,
                    auto_size_columns=True,
                    hide_vertical_scroll=False,
                    num_rows=20,
                    justification='center',
                    key='-TABLE-',
                    row_height=30,
                    alternating_row_color='#e0e0e0',
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                )
            else:
                tableElement = sg.Text(
                    'Não há dados para serem exibidos... Comece cadastrando-os!',
                    s=(40, 2),
                    justification='center'
                )

            return [
                [
                    sg.Column([
                        [
                            tableElement
                        ],

                        [
                            sg.Button(
                                f'Cadastrar',
                                key='btn_cadastrar',
                                size=(30, 2),
                                visible=btn_cadastrar_enabled
                            ),
                            sg.Column(
                                [
                                    buttons
                                ],
                                key='column_editar_deletar',
                                visible=False
                            )
                        ]

                    ], justification='center' if len(values) == 0 else 'left', vertical_alignment='center' if len(values) == 0 else 'top')
                ]
            ]

        return callable

    def validar_input(self, key: str, validator: bool, error_message: str) -> bool:
        hint = self._window.FindElement(key + '_hint')
        if validator:
            hint.Update(
                error_message,
                visible=True
            )
            return False
        else:
            hint.Update(visible=False)
            return True
