from models.models import Hospede, Session

def cadastra_hospede(nome, cpf, telefone, endereco, empresa):
    with Session() as session:
        try:
                hospede = Hospede(nome=nome, cpf=cpf, telefone=telefone, endereco=endereco, empresa=empresa)
                session.add(hospede)
                session.commit()
                return True
        except Exception as e:
            return False


def varifica_cpf_existe(cpf):
    with Session() as session:
        hospede = session.query(Hospede).filter(Hospede.cpf == cpf).first()
        if hospede:
            return True
        else:
            return False
        
def procura_hospede_completo(nome, empresa, telefone, endereco):
    with Session() as session:
        hospede = session.query(Hospede).filter_by(
                nome=nome, empresa=empresa, telefone=telefone, endereco=endereco
            ).first()
        if hospede:
            return hospede
        else:
            return []
        
def procura_hospedes_por_nome(nome):
    with Session() as session:
        hospedes = session.query(Hospede).filter(Hospede.nome.ilike(f"%{nome}%")).order_by(Hospede.nome).all()
        if hospedes:
            return hospedes
        else:
            return []
        
def procura_hospede_por_cpf(cpf):
    with Session() as session:
        hospede = session.query(Hospede).filter_by(cpf=cpf).first()
        if hospede:
            return hospede
        else:
            return []
        
def atualiza_hospede(cpf, nome, telefone, endereco, empresa):
    with Session() as session:
        hospede = session.query(Hospede).filter_by(cpf=cpf).first()
        if hospede:
            hospede.nome = nome
            hospede.telefone = telefone
            hospede.endereco = endereco
            hospede.empresa = empresa
            session.commit()
            return True
        else:
            return False