import re
import datetime
from brutils import cpf, cnpj


class Validators:

    def validar_nome(nome: str) -> bool:
        regex = '^[A-ZÀ-Ÿ][A-zÀ-ÿ\']+\s([A-zÀ-ÿ\']\s?)*[A-ZÀ-Ÿ][A-zÀ-ÿ\']+$'
        return True if re.search(regex, nome) else False

    def validar_cnpj(cnpj_string: str) -> bool:
        cnpj_formatado = cnpj.sieve(cnpj_string)
        return cnpj.validate(cnpj_formatado)

    def validar_cpf(cpf_string: str) -> bool:
        cpf_formatado = cpf.sieve(cpf_string)
        return cpf.validate(cpf_formatado)

    def validar_email(email: str) -> bool:
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        return True if re.search(regex, email) else False

    def validar_string(string: str) -> bool:
        regex = '^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ0-9 ]+$'
        return True if re.search(regex, string) else False

    def validar_numero(numero: str) -> bool:
        regex = '^([\s\d]+)$'
        return True if re.search(regex, numero) else False

    def validar_float(numero: str) -> bool:
        try:
            n = float(numero)
            return True
        except ValueError:
            return False

    def validar_telefone(telefone: str) -> bool:
        # Maneiras possíveis de inserir o telefone (DDD obrigatório):
        # (48) 2020-2020, (48) 20202020, (48) 32020-2020, (48) 320202020
        # 48 {valores acima}, 48{valores acima}, (48){valores acima}
        regex = '(\(?\d{2}\)?\s?)(\d{4,5}\-?\d{4})'
        return True if re.search(regex, telefone) else False

    def validar_cep(cep: str):
        regex = '(\d{5})-?(\d{3})'
        return True if re.search(regex, cep) else False

    def validar_data(data: str):
        try:
            datetime.datetime.strptime(data, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def validar_data_reatrotiva(data: str):
        if datetime.datetime.strptime(data, "%d/%m/%Y") <= datetime.datetime.now():
            return False
        else:
            return True

    def validar_data_min_3_days(data: str):
        min_date = datetime.datetime.strptime(
            data, "%d/%m/%Y") - datetime.timedelta(days=3)
        if min_date <= datetime.datetime.now():
            return False
        else:
            return True
