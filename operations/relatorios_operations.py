from models.models import Relatorio, Hospede, db
from utils.formatacao_de_entradas import formata_cpf
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db)
session = Session()

def relatorio_hospedagem():
    for hospedagem in session.query(Relatorio).all():
        nome = session.query(Hospede).filter_by(cpf=hospedagem.id_hospede).first().nome
        print('-'*50)
        print(f'CPF do Hóspede: {hospedagem.id_hospede}')
        print(f'Nome do Hóspede: {nome}')
        print(f'Número do Quarto: {hospedagem.id_quarto}')
        print(f'Data de Entrada: {hospedagem.data_entrada}')
        print(f'Data de Saída: {hospedagem.data_saida}')
        print(f'Valor Total: R$ {hospedagem.valor_total}')

def relatorio_hospedes():
    cliente = input("Digite o CPF do cliente: ")
    cliente = formata_cpf(cliente)
    cliente = session.query(Hospede).filter_by(cpf=cliente).first()
    if cliente:
        for hospedagem in session.query(Relatorio).filter_by(id_hospede=cliente.cpf).all():
            print('-'*50)
            print(f'CPF do Hóspede: {hospedagem.id_hospede}')
            print(f'Nome do Hóspede: {cliente.nome}')
            print(f'Número do Quarto: {hospedagem.id_quarto}')
            print(f'Data de Entrada: {hospedagem.data_entrada}')
            print(f'Data de Saída: {hospedagem.data_saida}')
            print(f'Valor Total: R$ {hospedagem.valor_total}')
        print('-'*50)
    else:
        print("Cliente não encontrado.")


def relatorio_diario():
    pass

