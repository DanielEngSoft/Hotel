from models.models import Hospedagem, Despesa, Produto, db  # Importa os modelos e a conexão com o banco
from sqlalchemy.orm import sessionmaker, joinedload         # Utilitários do SQLAlchemy
from sqlalchemy.exc import IntegrityError                   # Para tratar erros de integridade (ex: chaves duplicadas)
from models.models import Session as DBSession              # Session já configurada para consultas gerais
from datetime import datetime

# Cria uma fábrica de sessões do banco de dados
Session = sessionmaker(bind=db)



def create_despesa(id_hospedagem, id_produto, quantidade):
    try:
        with Session() as session:
            hospedagem = session.query(Hospedagem).filter_by(id=id_hospedagem).first()
            if not hospedagem:
                print(f"Hospedagem com ID {id_hospedagem} não encontrada.")
                return False

            produto = session.query(Produto).filter_by(id=id_produto).first()
            if not produto:
                print(f"Produto com ID {id_produto} não encontrado.")
                return False

            despesa = Despesa(
                id_hospedagem=id_hospedagem,
                id_produto=id_produto,
                quantidade=quantidade,
                valor=produto.valor * quantidade,
                data=datetime.now()
            )

            session.add(despesa)
            session.commit()
            return True

    except IntegrityError:
        session.rollback()
        print("Erro de integridade ao criar a despesa.")
        return False
    except Exception as e:
        session.rollback()
        print(f"Erro ao criar despesa: {e}")
        return False

from sqlalchemy.orm import joinedload

def buscar_despesas_por_id_hospedagem(id_hospedagem):
    with Session() as session:
        despesas = (
            session.query(Despesa)
            .options(joinedload(Despesa.produto))  # <- carrega o produto junto
            .filter(Despesa.id_hospedagem == id_hospedagem)
            .all()
        )
        return despesas
