from validate_docbr import CPF
import re

def valida_cpf(cpf):
    cpf_formatado = CPF()
    cpf = cpf.replace('.', '').replace('-', '')
    if cpf_formatado.validate(cpf):
        return True
    else:
        return False

def formata_nome(nome):
    return ' '.join(nome.split()).title().strip()

def valida_telefone(numero):
    teste = numero
    teste = re.sub(r'\D', '', teste)  # Remove não-dígitos
    print(teste)
    if len(teste) == 11:  # Com DDD e 9 dígitos
        return True
    else:  
        return False