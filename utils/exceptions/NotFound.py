class NotFound(Exception):
    def __init__(self):
        super().__init__('Item não encontrado')
