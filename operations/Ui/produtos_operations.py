from models.models import Produto, Quarto, Hospede, Session # Importa os modelos e a conexão com o banco
from sqlalchemy.orm import joinedload                       # Utilitários do SQLAlchemy
from sqlalchemy.exc import IntegrityError                   # Para tratar erros de integridade (ex: chaves duplicadas)
from utils.formatacao_de_entradas import formata_nome

def create_produto(descricao, valor):
    """Cria um novo produto."""
    with Session() as session:
        try:
            descricao = formata_nome(descricao)
            descricao = descricao.upper()
            produto = Produto(descricao=descricao, valor=valor)
            session.add(produto)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False

def listar_produtos():
    """Lista todos os produtos."""
    with Session() as session:
        produtos = session.query(Produto).order_by(Produto.descricao).all()
        return produtos

def buscar_produto_por_nome(descricao):
    """Busca um produto pelo nome."""
    with Session() as session:
        produto = session.query(Produto).filter(Produto.descricao.ilike(f"%{descricao}%")).order_by(Produto.descricao).all()
        return produto
    
def buscar_produto_por_id(id_produto):
    """Busca um produto pelo nome."""
    with Session() as session:
        produto = session.query(Produto).filter(Produto.id == id_produto).first()
        return produto
    
def update_produto(id_produto, descricao, valor):
    """Edita um produto existente."""
    with Session() as session:
        produto = session.query(Produto).filter(Produto.id == id_produto).first()
        try:
            if produto:
                produto.descricao = descricao
                produto.valor = valor
                session.commit()
                return True
            return False
        except IntegrityError:
            session.rollback()
            return False
        
def verifica_produto_existente(descricao):
    """Verifica se um produto com a mesma descrição já existe."""
    with Session() as session:
        produto = session.query(Produto).filter(Produto.descricao == descricao).first()
        if produto:
            return True
        return False
    
def selecionar_produto(descricao):
    """Seleciona um produto pelo nome."""
    with Session() as session:
        try:
            produto = session.query(Produto).filter(Produto.descricao == descricao).first()
            return produto
        except IntegrityError:
            session.rollback()
            return []