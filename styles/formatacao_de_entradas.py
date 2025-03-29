from validate_docbr import CPF
from datetime import datetime
import re

def formata_nome(nome):
    return ' '.join(nome.split()).title().strip()

def formata_cpf(cpf):
    cpf_formatado = CPF()
    cpf = cpf.replace('.', '').replace('-', '')
    while not cpf_formatado.validate(cpf):
        cpf = input("CPF inválido. Digite novamente: ")

    return cpf_formatado.mask(cpf)

def formata_telefone(telefone):
    while True:
        numero = telefone.replace('(', '').replace(')', '').replace('-', '').replace('.', '')
        numero = re.sub(r'\D', '', numero)  # Remove não-dígitos
        if len(numero) == 11:  # Com DDD e 9 dígitos
            return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
        elif len(numero) == 10:  # Com DDD e 8 dígitos
            return f"({numero[:2]}) {numero[2:6]}-{numero[6:]}"
        else:  # Retorna sem formatação se não se encaixar
            telefone = input("Telefone inválido. Digite novamente: ")

def formata_data(data):
    while True:
        try:
            data_formatada = datetime.strptime(data, "%d/%m/%Y")
            return data_formatada
        except ValueError:
            data = input("Data inválida. Digite novamente (dd/mm/aaaa): ")
