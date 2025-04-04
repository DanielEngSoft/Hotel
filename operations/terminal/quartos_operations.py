from models.models import Quarto, Hospedagem, db
from sqlalchemy.orm import sessionmaker
from os import system

Session = sessionmaker(bind=db)


def tipos_quartos():
    system('cls')
    while True:
        tipos = ['Solteiro', 'Casal', 'Casal + Solteiro', 'Casal + 2 Solteiros', '2 Solteiros', '3 Solteiros']
        print('-' * 50)
        print("Tipos de quartos disponíveis:")
        for i, tipo in enumerate(tipos):
            print(f"{i+1}) {tipo}")
        print('-' * 50)
        try:
            tipo_quarto = int(input("Escolha o tipo de quarto: "))
            if 1 <= tipo_quarto <= len(tipos):
                return tipos[tipo_quarto - 1]
            else:
                print("Opção inválida. Tente novamente.")
                system('pause')
                system('cls')
        except ValueError:
            print("Opção inválida. Tente novamente.")
            system('pause')
            system('cls')

def cadastrar_quarto():
    try:
        numero = int(input("Número do quarto: "))
    except ValueError:
        print("Número inválido.")
        return
    
    with Session() as session:
        if session.query(Quarto).filter_by(numero=numero).first():
            print("Quarto já cadastrado.")
            return
        tipo = tipos_quartos()
        quarto = Quarto(numero=numero, tipo=tipo, disponivel=True)
        session.add(quarto)
        session.commit()
        print("Quarto cadastrado com sucesso!")

def listar_quartos():
    system('cls')
    with Session() as session:
        quartos = session.query(Quarto).all()
        print('-' * 20,'Quartos', '-' * 20)
        for quarto in quartos:
            print(f"Número: {quarto.numero}, Tipo: {quarto.tipo}, Status: {'Disponivel 'if quarto.disponivel  else 'Ocupado'}")
            print('-' * 50)

def listar_quartos_disponiveis():
    system('cls')
    with Session() as session:
        quartos = session.query(Quarto).all()
        print('-' * 20,'Quartos Disponíveis', '-' * 20)
        for quarto in quartos:
            if quarto.disponivel == True:
                print(f"Número: {quarto.numero}, Tipo: {quarto.tipo}, Status: {'Disponivel 'if quarto.disponivel  else 'Ocupado'}")
                print('-' * 50)

def listar_quartos_ocupados():
    system('cls')
    with Session() as session:
        quartos = session.query(Quarto).all()
        print('-' * 20,'Quartos Ocupados', '-' * 20)
        for quarto in quartos:
            if quarto.disponivel == False:
                print(f"Número: {quarto.numero}, Tipo: {quarto.tipo}, Status: {'Disponivel 'if quarto.disponivel  else 'Ocupado'}")
                print('-' * 60)

def atualiza_tipo():
    numero = input("Digite o número do quarto: ")
    with Session() as session:
        quarto = session.query(Quarto).filter_by(numero=numero).first()
        if quarto:
            novo_tipo = tipos_quartos()
            quarto.tipo = novo_tipo
            session.commit()
            print("Tipo atualizado com sucesso!")
        else:
            print("Quarto não encontrado.")

def atualiza_status():
    numero = input("Digite o número do quarto: ")
    with Session() as session:
        quarto = session.query(Quarto).filter_by(numero=numero).first()
        if quarto:
            if quarto.disponivel == True:
                quarto.disponivel = False
            else:
                quarto.disponivel = True
            session.commit()
            print("Status atualizado com sucesso!")
        else:
            print("Quarto não encontrado.")

def excluir_quarto():
    numero = input("Digite o número do quarto: ")
    with Session() as session:
        quarto = session.query(Quarto).filter_by(numero=numero).first()
        if quarto:
            if session.query(Hospedagem).filter_by(id_quarto=numero).first():
                print("Não é possível excluir o quarto pois há hospedagens associadas a ele.")
                return
            else:
                session.delete(quarto)
                session.commit()
                print("Quarto excluído com sucesso!")
        else:
            print("Quarto não encontrado.")