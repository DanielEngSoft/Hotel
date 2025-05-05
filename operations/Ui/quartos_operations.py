from sqlalchemy.orm import Session, sessionmaker
from models.models import Quarto, Hospedagem, Reserva, db
from sqlalchemy.exc import IntegrityError

Session = sessionmaker(bind=db)

def cadastra_quarto(num, tipo):
    with Session() as session:
        try:
                num = int(num)
                quarto = Quarto(numero=num, tipo=tipo, disponivel=True)
                session.add(quarto)
                session.commit()
                return True
        except IntegrityError:
            session.rollback()
            return False
        except Exception as e:
            session.rollback()
            print(f"Erro ao criar quarto: {e}")
            return False
    
def listar_quartos():
    with Session() as session:
        try:
                quartos = session.query(Quarto).all()
                return quartos
        except Exception as e:
            print(f"Erro ao listar quartos: {e}")
            return False
    
def listar_quartos_disponiveis():
    with Session() as session:
        try:
            quartos = session.query(Quarto).filter(Quarto.disponivel == True).all()
            return quartos
        except Exception as e:
            print(f"Erro ao listar quartos disponíveis: {e}")
            return False


def qtd_disponiveis():
    with Session() as session:
        try:
            quartos = session.query(Quarto).filter(Quarto.disponivel == True).count()
            return quartos
        except Exception as e:
            print(f"Erro ao listar quartos disponíveis: {e}")
            return False


def qtd_ocupados():
    with Session() as session:
        try:
            quartos = session.query(Quarto).filter(Quarto.disponivel == False).count()
            return quartos
        except Exception as e:
            print(f"Erro ao listar quartos ocupados: {e}")
            return False


def listar_quartos_ocupados():
    with Session() as session:
        try:
            quartos = session.query(Quarto).filter(Quarto.disponivel == False).all()
            return quartos
        except Exception as e:
            print(f"Erro ao listar quartos ocupados: {e}")
            return False

def verifica_quarto_existe(numero):
    with Session() as session:
        return session.query(Quarto).filter(Quarto.numero == numero).first()
    
def quarto_por_id_hospedagem(id_hospedagem):
    with Session() as session:
        try:
            quarto = session.query(Quarto).join(Hospedagem).filter(Hospedagem.id == id_hospedagem).first()
            return quarto
        except Exception as e:
            print(f"Erro ao buscar quarto por ID da hospedagem: {e}")
            return None
    
def alterar_quarto(numero, tipo):
    with Session() as session:
        try:
            quarto = session.query(Quarto).filter(Quarto.numero == numero).first()
            if quarto:
                quarto.tipo = tipo
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Erro ao alterar quarto: {e}")
            return False

def listar_quartos_por_data(data_entrada, data_saida):
    with Session() as session:
        try:
            # Todos os quartos cadastrados
            todos_quartos = session.query(Quarto).all()

            # Quartos com reservas no período
            quartos_reservados = session.query(Quarto).join(Reserva).filter(
                Reserva.data_entrada <= data_saida,
                Reserva.data_saida >= data_entrada
            ).all()

            # Quartos com hospedagens no período
            quartos_hospedados = session.query(Quarto).join(Hospedagem).filter(
                Hospedagem.data_entrada <= data_saida,
                Hospedagem.data_saida >= data_entrada
            ).all()

            # IDs dos quartos ocupados (por reserva ou hospedagem)
            quartos_ocupados_ids = {q.numero for q in quartos_reservados + quartos_hospedados}

            # Filtra os disponíveis
            quartos_disponiveis = [q for q in todos_quartos if q.numero not in quartos_ocupados_ids]

            # Ordena por número
            return sorted(quartos_disponiveis, key=lambda x: x.numero)

        except Exception as e:
            print(f"Erro ao listar quartos disponíveis por data: {e}")
            return 0
