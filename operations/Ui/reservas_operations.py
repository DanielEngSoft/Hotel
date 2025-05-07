from sqlalchemy.orm import Session, sessionmaker, joinedload
from models.models import Reserva, db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

Session = sessionmaker(bind=db)

def create_reserva(id_hospede, id_quarto, data_entrada, data_saida, qtd_hospedes, acompanhantes, adiantamento, valor_diaria, obs):
    with Session() as session:
        try:
            reserva = Reserva(
                id_hospede=id_hospede,
                id_quarto=id_quarto,
                data_entrada=data_entrada,
                data_saida=data_saida,
                qtd_hospedes=qtd_hospedes,
                acompanhantes=acompanhantes,
                adiantamento=adiantamento,
                valor_diaria=valor_diaria,
                obs=obs
            )
            session.add(reserva)            
            session.commit()
            session.close()
            return True
        except IntegrityError:
            session.rollback()
            return False
        
def reservas_ativas():
    with Session() as session:
        # Consulta todas as hospedagens, carregando também os dados relacionados (quarto e hóspede)
        reservas = session.query(Reserva)\
            .options(
                joinedload(Reserva.quarto),   # Carrega automaticamente os dados do quarto
                joinedload(Reserva.hospede)   # Carrega automaticamente os dados do hóspede
            ).all()

        # Retorna a lista de objetos Hospedagem
        return reservas