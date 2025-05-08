from sqlalchemy.orm import Session, sessionmaker, joinedload
from models.models import Reserva,Hospedagem, db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from operations.Ui.hospedagem_operations import create_hospedagem, adicionar_adiantamento
from operations.Ui.produtos_operations import buscar_produto_por_id

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
            ).order_by(Reserva.data_entrada).all()

        # Retorna a lista de objetos Hospedagem
        return reservas
    
def reserva_para_hospedagem(id_reserva):
    with Session() as session:
        reserva = session.query(Reserva).filter_by(id_reserva=id_reserva).first()
        if reserva:
            produto = buscar_produto_por_id(reserva.qtd_hospedes)
            valor_diaria = produto.valor

            create_hospedagem(id_hospede=reserva.id_hospede,id_quarto=reserva.id_quarto, 
                data_saida=reserva.data_saida, qtd_hospedes=reserva.qtd_hospedes, 
                valor_diaria=valor_diaria,obs=reserva.obs, acompanhantes=reserva.acompanhantes)

