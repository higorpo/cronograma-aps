import os
import PySimpleGUI as sg


class TelaMensagemSistema:
    def __init__(self, controlador):
        self.__controlador_sistema = controlador

    def warning(self, message: str) -> None:
        # Printa uma mensagem de aviso
        sg.popup_ok(message, title='Aviso')

    def success(self, message: str) -> None:
        # Printa uma mensagem de sucesso
        sg.popup_ok(message, title='Sucesso')

    def error(self, message: str) -> None:
        # Printa uma mensagem de erro
        sg.popup_error(message, title='Erro')

    def info(self, message: str) -> None:
        # Printa uma mensagem de informação
        sg.popup_ok(message, title='Info')

    def log(self, message: str) -> None:
        # Print um log normal
        sg.popup_ok(message, title='Info')
