import re
from brutils import cpf, cnpj


class Formatters:
    def formatar_telefone(telefone: str):
        tel_soh_numeros = ''.join(re.findall('\d+', telefone))
        lista_pra_formatar = list(tel_soh_numeros)
        lista_pra_formatar.insert(0, '(')
        lista_pra_formatar.insert(3, ')')
        lista_pra_formatar.insert(4, ' ')
        lista_pra_formatar.insert(-4, '-')
        telefone_formatado = ''.join(lista_pra_formatar)
        return telefone_formatado

    def formatar_cep(cep: str):
        cep_soh_numeros = ''.join(re.findall('\d+', cep))
        lista_numeros_do_cep = list(cep_soh_numeros)
        lista_numeros_do_cep.insert(-3, '-')
        cep_formatado = ''.join(lista_numeros_do_cep)
        return cep_formatado

    def formatar_cpf(inputed_cpf: str):
        if '.' not in inputed_cpf:
            inputed_cpf = cpf.display(inputed_cpf)
        return inputed_cpf

    def formatar_cnpj(inputed_cnpj: str):
        if '.' not in inputed_cnpj:
            inputed_cnpj = cnpj.display(inputed_cnpj)
        return inputed_cnpj
