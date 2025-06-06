from models.models import Hospedagem, Despesa, Produto, Session # Importa os modelos e a conexão com o banco
from sqlalchemy.orm import joinedload         # Utilitários do SQLAlchemy
from sqlalchemy.exc import IntegrityError                   # Para tratar erros de integridade (ex: chaves duplicadas)
from datetime import datetime

def create_despesa(id_hospedagem, id_produto, quantidade, valor_produto, data=None):
    with Session() as session:
        try:
            hospedagem = session.query(Hospedagem).filter_by(id=id_hospedagem).first()
            if not hospedagem:
                print(f"Hospedagem com ID {id_hospedagem} não encontrada.")
                return []

            produto = session.query(Produto).filter_by(id=id_produto).first()
            if not produto:
                print(f"Produto com ID {id_produto} não encontrado.")
                return []

            valor_total = quantidade * valor_produto
            if data is None:
                data = datetime.now()
                
            despesa = Despesa(
                id_hospedagem=id_hospedagem,
                id_produto=id_produto,
                quantidade=quantidade,
                valor_produto=valor_produto,
                valor=valor_total,
                data=data
            )

            session.add(despesa)
            session.commit()
            session.refresh(despesa)  # <- ESSENCIAL para garantir que o objeto está completo
            return despesa  # <- Aqui está a mudança principal

        except IntegrityError:
            session.rollback()
            print("Erro de integridade ao criar a despesa.")
            return []

        except Exception as e:
            session.rollback()
            print(f"Erro ao criar despesa: {e}")
            return []

        finally:
            session.close()


def buscar_despesas_por_id_hospedagem(id_hospedagem):
    with Session() as session:
        despesas = (
            session.query(Despesa)
            .options(joinedload(Despesa.produto))  # <- carrega o produto junto
            .filter(Despesa.id_hospedagem == id_hospedagem)
            .order_by(Despesa.data)
            .all()
        )
        return despesas    
def somar_despesas(id_hospedagem):
    with Session() as session:
        try:
            despesas = (
                session.query(Despesa)
                .filter(Despesa.id_hospedagem == id_hospedagem)
                .all()
            )
            total = sum(despesa.valor for despesa in despesas)
            return total
        except Exception as e:
            print(f"Erro ao somar despesas: {e}")
            return 0.0
            
