from sqlalchemy.orm import Session
from models.models import Quarto
from sqlalchemy.exc import IntegrityError

def create_quarto(num, tipo):
    try:
        with Session() as session:
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
    try:
        with Session() as session:
            quartos = session.query(Quarto).all()
            return quartos
    except Exception as e:
        print(f"Erro ao listar quartos: {e}")
        return []
    
def listar_quartos_disponiveis():
    try:
        with Session() as session:
            quartos = session.query(Quarto).filter(Quarto.disponivel == True).all()
            return quartos
    except Exception as e:
        print(f"Erro ao listar quartos disponíveis: {e}")
        return 'erro'

def listar_quartos_ocupados():
    try:
        with Session() as session:
            quartos = session.query(Quarto).filter(Quarto.disponivel == False).all()
            return quartos
    except Exception as e:
        print(f"Erro ao listar quartos ocupados: {e}")
        return []