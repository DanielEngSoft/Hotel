from sqlalchemy.orm import Session, sessionmaker
from models.models import Quarto, db
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
        quartos = session.query(Quarto).filter_by(disponivel=True).all()
        return quartos

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