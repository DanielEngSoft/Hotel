from models.models import Funcionario, db
from sqlalchemy.orm import sessionmaker
from os import system

Session = sessionmaker(bind=db)

def cadastrar_funcionario():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    telefone = input("Telefone: ")

    funcionario = Funcionario(nome=nome, cpf=cpf, telefone=telefone)
    with Session() as session:
        session.add(funcionario)
        session.commit()

def listar_funcionarios():
    system('cls')
    with Session() as session:
        funcionarios = session.query(Funcionario).all()
        for funcionario in funcionarios:
            print('-'*70)
            print(f"ID: {funcionario.id}, Nome: {funcionario.nome}, CPF: {funcionario.cpf}, Telefone: {funcionario.telefone}")
        print('-'*70)

def atualizar_funcionario():
    id = int(input("Digite o ID do funcionário que deseja atualizar: "))
    with Session() as session:
        funcionario = session.query(Funcionario).filter_by(id=id).first()
        if funcionario:
            funcionario.nome = input("Novo nome: ")
            funcionario.cpf = input("Novo CPF: ")
            funcionario.telefone = input("Novo telefone: ")
            funcionario.cargo = input("Novo cargo: ")
            session.commit()
            print("Funcionário atualizado com sucesso!")
        else:
            print("Funcionário não encontrado.")
        
def excluir_funcionario():
    cpf = input("Digite o CPF do funcionário que deseja excluir: ")
    with Session() as session:
        funcionario = session.query(Funcionario).filter_by(cpf=cpf).first()
        if funcionario:
            session.delete(funcionario)
            session.commit()
            print("Funcionário excluído com sucesso!")
        else:
            print("Funcionário não encontrado.")