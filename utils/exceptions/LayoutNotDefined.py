class LayoutNotDefined(Exception):
    def __init__(self):
        super().__init__('Layout não definido')
