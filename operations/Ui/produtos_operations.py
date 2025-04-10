from models.models import Produto, Quarto, Hospede, db  # Importa os modelos e a conexão com o banco
from sqlalchemy.orm import sessionmaker, joinedload        # Utilitários do SQLAlchemy
from sqlalchemy.exc import IntegrityError                  # Para tratar erros de integridade (ex: chaves duplicadas)
from models.models import Session as DBSession             # Session já configurada para consultas gerais

# Cria uma fábrica de sessões do banco de dados
Session = sessionmaker(bind=db)

def buscar_produto_por_nome(nome_produto):
    """Busca um produto pelo nome."""
    with Session() as session:
        produto = session.query(Produto).filter(Produto.descricao.ilike(f"%{nome_produto}%")).limit(5).all()
        return produto
