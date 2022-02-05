import json
from datetime import datetime, timedelta
from os.path import abspath
from time import time

from model.Atividade import Atividade

FILE_LOCATION = abspath('dao/store/cronograma.json')


class CronogramaDAO:
    def __init__(self):
        # Opening JSON file
        with open(FILE_LOCATION, 'r') as openfile:
            self.__data: dict = json.load(openfile)

    def save_all(self):
        with open(FILE_LOCATION, 'w') as openfile:
            json.dump(self.__data, openfile)

    def add_atividade(self, atividade: Atividade):
        mensagens_retorno = None

        # Verifica nível de dificuldade da atividade
        minutos_por_grau_dificuldade = {
            'fácil': 30,
            'médio': 60,
            'díficil': 90,
            'muito difícil': 120
        }

        # Tempo necessário para executar a atividade
        tempo_necessario = minutos_por_grau_dificuldade[atividade.grau_dificuldade]

        # Quantidade de blocos de 30 minutos que precisam ser alocados
        blocos_para_alocar = int(tempo_necessario / 30)

        # Configurando as datas do prazo de entrega da atividade menos os dois dias mínimos necessários
        prazo_entrega_datetime = datetime.strptime(
            atividade.prazo_entrega, "%d/%m/%Y"
        ) - timedelta(days=3)

        # Pega o momento atual
        agora = datetime.now()

        # Se de início das buscas for igual a data atual, então aloca todos os blocos para o dia de hoje e emite um alarta
        if prazo_entrega_datetime.day == agora.day and prazo_entrega_datetime.month == agora.month and prazo_entrega_datetime.year == agora.year:
            print('O período de buscas é igual a data atual')
            for i in range(blocos_para_alocar):
                # Aloca os blocos de estudos
                self.alocar_atividade_em_data(
                    agora.day,
                    agora.month,
                    agora.year,
                    atividade
                )

            self.save_all()

            # Verifica se estourou o máximo de blocos de estudos por dias
            if len(self.get_atividades_na_data(agora.day, agora.month, agora.year)) > 8:
                print(
                    f'Alocado mais blocos no dia {agora.day}/{agora.month}/{agora.year} do que o habitual'
                )
                mensagens_retorno = f'Alocado mais blocos na data {agora.day}/{agora.month}/{agora.year} do que o habitual'

            return mensagens_retorno

        datas_para_alocar = self.verifica_dias_possivel_para_alocar(
            atividade,
            blocos_para_alocar,
            1
        )

        if len(datas_para_alocar) >= blocos_para_alocar:
            # Aloca os blocos nas datas determinadas.
            for data in datas_para_alocar:
                self.alocar_atividade_em_data(
                    data[0],
                    data[1],
                    data[2],
                    atividade
                )

            self.save_all()

            return None
        else:
            print('Não há dias suficientes para alocar todos os blocos necessários')

            # Se houver apenas um bloco para alocar, então aloca tudo no mesmo dia.
            if blocos_para_alocar == 1:
                print(
                    f'Alocamos então no dia {prazo_entrega_datetime.day}/{prazo_entrega_datetime.month}/{prazo_entrega_datetime.year}'
                )
                self.alocar_atividade_em_data(
                    prazo_entrega_datetime.day, prazo_entrega_datetime.month, prazo_entrega_datetime.year, atividade
                )

                # Verifica se estourou o máximo de blocos de estudos por dias
                if len(self.get_atividades_na_data(prazo_entrega_datetime.day, prazo_entrega_datetime.month, prazo_entrega_datetime.year)) > 8:
                    print(
                        f'Alocado mais blocos no dia {prazo_entrega_datetime.day} do que o habitual'
                    )
                    mensagens_retorno = f'Alocado mais blocos no data {prazo_entrega_datetime.day}/{prazo_entrega_datetime.month}/{prazo_entrega_datetime.year} do que o habitual'

                self.save_all()

                return mensagens_retorno
            else:
                # Se for mais de um bloco, então verifica se consegue então alocar tudo com 2 blocos por dia
                datas_para_alocar = self.verifica_dias_possivel_para_alocar(
                    atividade,
                    blocos_para_alocar / 2,
                    2
                )

                if len(datas_para_alocar) >= blocos_para_alocar / 2:
                    # Aloca os blocos nas datas determinadas.
                    for data in datas_para_alocar:
                        # Aloca duas vezes dentro desse dia.
                        self.alocar_atividade_em_data(
                            data[0],
                            data[1],
                            data[2],
                            atividade
                        )
                        self.alocar_atividade_em_data(
                            data[0],
                            data[1],
                            data[2],
                            atividade
                        )

                    print(
                        'Atividade alocada com dois blocos de estudo por dia sem estourar o máximo de 8 blocos diários.'
                    )

                    self.save_all()

                    return 'Atividade alocada com dois blocos de estudo por dia sem estourar o máximo de 8 blocos diários.'
                else:
                    print('Ainda assim não conseguiu alocar.')

                    # Aloca então, 1 bloco por dia, mesmo que ele ultrapasse o máximo de 8 blocos por dia.
                    datas_para_alocar = self.verifica_dias_possivel_para_alocar(
                        atividade,
                        blocos_para_alocar,
                        1,
                        True
                    )

                    # Aloca os blocos nas datas determinadas.
                    for data in datas_para_alocar:
                        # Aloca duas vezes dentro desse dia.
                        self.alocar_atividade_em_data(
                            data[0],
                            data[1],
                            data[2],
                            atividade
                        )

                    if len(datas_para_alocar) < blocos_para_alocar:
                        qtd_restante = blocos_para_alocar - \
                            len(datas_para_alocar)
                        data_atual = datetime.now()
                        print(
                            f'Ainda faltaram {qtd_restante} blocos para alocar'
                        )
                        for i in range(qtd_restante):
                            print(
                                f'> Alocando em {data_atual.day}/{data_atual.month}/{data_atual.year}'
                            )
                            self.alocar_atividade_em_data(
                                data_atual.day,
                                data_atual.month,
                                data_atual.year,
                                atividade
                            )
                            data_atual = data_atual + timedelta(days=1)

                    print(
                        'Atividade alocada com um bloco por dia com a possibilidade de estourar o máximo de 8 blocos diários.'
                    )

                    self.save_all()

                    return 'Atividade alocada com um bloco por dia com a possibilidade de estourar o máximo de 8 blocos diários.'

    def alocar_atividade_em_data(self, dia, mes, ano, atividade: Atividade):
        atividade.add_data_alocado(dia, mes, ano)
        self.set_value_to_data(dia, mes, ano, str(atividade.id))

    def get_atividades_na_data(self, dia, mes, ano):
        atividades_alocadas_no_dia = self.__data \
            .get(str(ano), {}) \
            .get(str(mes), {}) \
            .get(str(dia), [])

        return atividades_alocadas_no_dia

    def deleta_atividade_na_data(self, dia, mes, ano, atividade):
        try:
            self.__data[str(ano)][str(mes)][str(dia)] = list(
                filter((str(atividade.id)).__ne__, self.__data[str(ano)][str(mes)][str(dia)]))
            self.save_all()
        except Exception:
            print('Um erro ocorreu!')

    def deleta_alocacao_atividade(self, atividade: Atividade):
        for [dia, mes, ano] in atividade.datas_alocado():
            print('Deletando atividade no: ', dia, mes, ano)
            self.deleta_atividade_na_data(dia, mes, ano, atividade)

    def pode_alocar_atividade_em_data(self, dia, mes, ano, blocos_por_dia):
        return len(self.get_atividades_na_data(dia, mes, ano)) < 8 - (blocos_por_dia - 1)

    def set_value_to_data(self, dia, mes, ano, atividade_id):
        d_ano = self.__data.get(str(ano), {})
        d_mes = d_ano.get(str(mes), {})
        d_dia = d_mes.get(str(dia), [])

        if self.__data.get(str(ano), None) is None:
            self.__data[str(ano)] = {}
        if self.__data[str(ano)].get(str(mes), None) is None:
            self.__data[str(ano)][str(mes)] = {}

        self.__data[str(ano)][str(mes)][str(dia)] = d_dia + [atividade_id]

    def verifica_dias_possivel_para_alocar(self, atividade: Atividade, blocos_para_alocar: int, blocos_por_dia: int, pode_ultrapassar_8_blocos: bool = False):
        # Executa um looping verificando se da primeira data possível para
        # alocar até a data atual é possível adicionar os blocos necessários
        procurando_datas_para_alocar = True

        datas_para_alocar = []

        # Configurando as datas do prazo de entrega da atividade menos os dois dias mínimos necessários
        prazo_entrega_datetime = datetime.strptime(
            atividade.prazo_entrega, "%d/%m/%Y"
        ) - timedelta(days=3)

        # Pega o momento atual
        agora = datetime.now()

        while procurando_datas_para_alocar:
            prazo_igual_agora = prazo_entrega_datetime.day == agora.day and prazo_entrega_datetime.month == agora.month and prazo_entrega_datetime.year == agora.year

            # Se a data de busca chegar até a data atual, então para as buscas
            if prazo_igual_agora:
                procurando_datas_para_alocar = False

            # Data em que é possível começar a alocar blocos de estudo
            p_dia = prazo_entrega_datetime.day
            p_mes = prazo_entrega_datetime.month
            p_ano = prazo_entrega_datetime.year

            # Verifica se é possível alocar uma atividade para essa data
            if self.pode_alocar_atividade_em_data(p_dia, p_mes, p_ano, blocos_por_dia) or pode_ultrapassar_8_blocos:
                print('Encontrou disponível em ', p_dia, p_mes, p_ano)
                # Informa a possibilidade de alocar blocos nessa datas
                datas_para_alocar.append([p_dia, p_mes, p_ano])

                # Verifica se precisa de mais dias para alocar blocos
                if len(datas_para_alocar) == blocos_para_alocar:
                    # Encerra a procura por datas
                    procurando_datas_para_alocar = False
                    break

            # Vai progressivamente diminuindo a data
            prazo_entrega_datetime = prazo_entrega_datetime - \
                timedelta(days=1)

        return datas_para_alocar
