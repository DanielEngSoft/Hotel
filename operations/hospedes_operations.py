from models.models import Hospede, Hospedagem, db
from sqlalchemy.orm import sessionmaker

from os import system

from styles.formatacao_de_entradas import formata_cpf, formata_nome, formata_telefone

Session = sessionmaker(bind=db)
session = Session()
    
def cadastrar_hospede():
    cpf = input("CPF: ")
    cpf = formata_cpf(cpf)
    if session.query(Hospede).filter_by(cpf=cpf).first():
        print("Hóspede já cadastrado.")
        return
    else:
        nome = input("Nome: ") 
        nome = formata_nome(nome)

        telefone = input("Telefone: ")
        telefone = formata_telefone(telefone)

        hospede = Hospede(nome=nome, cpf=cpf, telefone=telefone)

        session.add(hospede)
        session.commit()
        return hospede

def listar_hospedes():
    system('cls')
    hospedes = session.query(Hospede).all()
    for hospede in hospedes:
        print('-'*83)
        print(f"ID: {hospede.id}, Nome: {hospede.nome}, CPF: {hospede.cpf}, Telefone: {hospede.telefone}")
    print('-'*83)

def atualizar_hospede():
    cpf = input("Digite o CPF do hóspede que deseja atualizar: ")
    cpf = formata_cpf(cpf)

    hospede = session.query(Hospede).filter_by(cpf=cpf).first()
    if hospede:
        hospede.nome = input("Novo nome: ")
        hospede.nome = formata_nome(hospede.nome)

        hospede.cpf = input("Novo CPF: ")
        hospede.cpf = formata_cpf(hospede.cpf)

        hospede.telefone = input("Novo telefone: ")
        hospede.telefone = formata_telefone(hospede.telefone)

        session.commit()
        print("Hóspede atualizado com sucesso!")
        return hospede
    
    else:
        print("Hóspede não encontrado.")

def excluir_hospede():
    id = input("ID do hóspede a ser excluído: ")
    hospede = session.query(Hospede).filter_by(id=id).first()
    if hospede:
        if session.query(Hospedagem).filter_by(id_hospede=hospede.cpf).all():
            print("impossievel excluir hospede com hospedagem(ns) ativa(s).")
            print("Feche as hospedagens ativas antes de excluir o hóspede.")
            return
        confirmar = input(f"Tem certeza que deseja excluir o hóspede {hospede.nome}? (S/N): ")
        if confirmar.lower() != 's':
            return
        else:
            session.delete(hospede)
            session.commit()
            print("Hóspede excluído com sucesso!")

    else:
        print("Hóspede não encontrado.")