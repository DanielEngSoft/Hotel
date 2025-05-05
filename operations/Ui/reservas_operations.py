from sqlalchemy.orm import Session, sessionmaker
from models.models import Reserva,Hospedagem, db
from sqlalchemy.exc import IntegrityError

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