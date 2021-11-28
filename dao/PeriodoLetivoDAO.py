import uuid

from dao.AbstractDAO import DAO
from model.PeriodoLetivo import PeriodoLetivo


class PeriodoLetivoDAO(DAO):
    def __init__(self):
        super().__init__('dao/store/periodo_letivo.pkl')

    def add(self, periodo_letivo: PeriodoLetivo):
        if ((periodo_letivo is not None) and isinstance(periodo_letivo, PeriodoLetivo) and isinstance(periodo_letivo.id, uuid.UUID)):
            super().add(periodo_letivo.id, periodo_letivo)

    def remove(self, periodo_letivo: PeriodoLetivo):
        if ((periodo_letivo is not None) and isinstance(periodo_letivo, PeriodoLetivo) and isinstance(periodo_letivo.id, uuid.UUID)):
            super().remove(periodo_letivo.id)
