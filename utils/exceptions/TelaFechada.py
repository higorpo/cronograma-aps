class TelaFechada(Exception):
    def __init__(self):
        super().__init__('Tela foi fechada')
