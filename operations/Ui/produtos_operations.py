from models.models import Produto, Quarto, Hospede, Session # Importa os modelos e a conexão com o banco
from sqlalchemy.orm import joinedload                       # Utilitários do SQLAlchemy
from sqlalchemy.exc import IntegrityError                   # Para tratar erros de integridade (ex: chaves duplicadas)

def buscar_produto_por_nome(nome_produto):
    """Busca um produto pelo nome."""
    with Session() as session:
        produto = session.query(Produto).filter(Produto.descricao.ilike(f"%{nome_produto}%")).all()
        return produto
    
def buscar_produto_por_id(id_produto):
    """Busca um produto pelo nome."""
    with Session() as session:
        produto = session.query(Produto).filter(Produto.id == id_produto).first()
        return produto