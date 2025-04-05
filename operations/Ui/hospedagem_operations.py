from models.models import Hospedagem,Quarto, Hospede, db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

def diaria(pessoas):
    if pessoas == 1:
        return 100
    elif pessoas == 2:
        return 150
    elif pessoas == 3:
        return 200
    elif pessoas == 4:
        return 250
    else:
        return pessoas * 60
    

def create_hospedagem(id_hospede, id_quarto, data_saida, qtd_hospedes):
        try:
            with sessionmaker(bind=db)() as session:
                # Verifica se o quarto está disponível
                quarto = session.query(Quarto).filter_by(numero=id_quarto).first()
                if not quarto or not quarto.disponivel:
                    return False
                
                # Verifica se o hóspede existe
                hospede = session.query(Hospede).filter_by(cpf=id_hospede).first()
                if not hospede:
                    return False

                hospedagem = Hospedagem(
                    id_hospede=id_hospede,
                    id_quarto=id_quarto,
                    data_saida=data_saida,
                    qtd_hospedes=qtd_hospedes,
                    valor_diaria=diaria(qtd_hospedes)
                )
                quarto = session.query(Quarto).filter_by(numero=id_quarto).first()
                session.add(hospedagem)
                quarto.disponivel = False
                session.commit()
                return True
        except IntegrityError:
            session.rollback()
            return False
        except Exception as e:
            session.rollback()
            print(f"Erro ao criar hospedagem: {e}")
            return False