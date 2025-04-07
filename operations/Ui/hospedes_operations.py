from sqlalchemy.orm import sessionmaker
from models.models import Hospede, db

def cadastra_hospede(nome, cpf, telefone, endereco, empresa):
    try:
        Session = sessionmaker(bind=db.engine)
        with Session() as session:
            hospede = Hospede(nome=nome, cpf=cpf, telefone=telefone)
            session.add(hospede)
            session.commit()
            return True
    except Exception as e:
        return False


def varifica_cpf_existe(cpf):
    Session = sessionmaker(bind=db.engine)
    with Session() as session:
        hospede = session.query(Hospede).filter(Hospede.cpf == cpf).first()
        if hospede:
            return True
        else:
            return False