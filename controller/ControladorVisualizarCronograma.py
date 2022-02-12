from uuid import UUID, uuid4
from dao.AtividadeDAO import AtividadeDAO
from dao.CronogramaDAO import CronogramaDAO
from messages.Atividade import mensagens_atividade
from view.TelaVisualizarCronograma import TelaVisualizarCronograma
from datetime import datetime, timedelta


class ControladorVisualizarCronograma:
    __instance = None

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaVisualizarCronograma(self)
        self.__atividade_dao = AtividadeDAO()
        self.__cronograma_dao = CronogramaDAO()

    def __new__(cls, _):
        if ControladorVisualizarCronograma.__instance is None:
            ControladorVisualizarCronograma.__instance = object.__new__(cls)
        return ControladorVisualizarCronograma.__instance

    @property
    def atividade_dao(self) -> AtividadeDAO:
        return self.__atividade_dao

    @property
    def cronograma_dao(self) -> CronogramaDAO:
        return self.__cronograma_dao

    def abre_tela(self):
        while True:
            event, values = self.__tela.abrir_tela(
                self.map_atividades_to_dict())
            print(values)
            if event == 'exited':
                break
            elif 'criar_' in event:
                # Redireciona para a tela de criar anotações
                print('texto criar nota foi clicado')
            elif 'concluir_' in event:
                # Abre tela de concluir atividade
                print('texto concluir foi clicado')
            elif 'excluir_' in event:
                self.__tela.fechar_tela()
                self.excluir(values)

    def map_atividades_to_dict(self):

        dict_atividades_da_semana = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
        }

        semana_atual = self.get_week_dates(datetime.today(), 1, 7)

        lista_dias_da_semana_formatados = []
        for data in semana_atual:
            dia = f'0{data[0]}' if data[0] < 10 else f'{data[0]}'
            mes = f'0{data[1]}' if data[1] < 10 else f'{data[1]}'
            lista_dias_da_semana_formatados.append(f'{dia}/{mes}')

        for i in range(7):
            #print(f'Dia da semana: {lista_dias_da_semana_formatados[i]}')
            lista_id_atividades_do_dia = self.__cronograma_dao.get_atividades_na_data(
                semana_atual[i][0], semana_atual[i][1], semana_atual[i][2])

            lista_todas_atividades = self.__atividade_dao.get_all()

            lista_obj_atividades = []

            for atividade in lista_todas_atividades:
                if str(atividade.id) in lista_id_atividades_do_dia:
                    lista_obj_atividades.append(atividade)

            dict_atividades_da_semana[i] = list(
                map(lambda atividade: {
                    'nome': atividade.nome,
                    'prazo_entrega': atividade.prazo_entrega,
                    'tag': atividade.tag.nome,
                    'id': str(atividade.id),
                    'tempo': lista_id_atividades_do_dia.count(str(atividade.id))
                }, lista_obj_atividades))

        dict_data = {
            'dias_semana': lista_dias_da_semana_formatados,
            'atividades': dict_atividades_da_semana
        }

        return dict_data

    def get_week_dates(self, base_date, start_day, end_day=None):
        monday = base_date - timedelta(days=base_date.isoweekday() - 1)
        week_dates = [monday + timedelta(days=i) for i in range(7)]
        formatted_dates = week_dates[start_day - 1:end_day or start_day]
        return list(map(lambda data: [data.day, data.month, data.year], formatted_dates))

    # TODO: implentar lógica para criar nota (provavelmente só redireciona)
    def criar_nota(self):
        return NotImplementedError

    # TODO: implentar lógica para concluir a atividade
    def concluir(self):
        return NotImplementedError

    def excluir(self, codigo_atividade: str):
        try:
            atividade = self.__atividade_dao.get(UUID(codigo_atividade))
            self.__cronograma_dao.deleta_alocacao_atividade(atividade)
            self.__atividade_dao.remove(atividade)
        except Exception:
            self.__controlador_sistema\
                .mensagem_sistema.error(mensagens_atividade.get('erro_excluir'))
