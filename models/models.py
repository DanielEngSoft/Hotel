from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

# Configuração do banco
db = create_engine('sqlite:///data/hp-prime.db')
Base = declarative_base()
Session = sessionmaker(bind=db)


class Hospedagem(Base):
    __tablename__ = 'hospedagens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_hospede = Column(String, ForeignKey('hospedes.cpf')) 
    id_quarto = Column(Integer, ForeignKey('quartos.numero'))
    data_entrada = Column(DateTime, default=datetime.datetime.now)
    data_saida = Column(DateTime)
    qtd_hospedes = Column(Integer)
    valor_diaria = Column(Float)
    aberta = Column(Boolean, default=True)  # True se a hospedagem estiver aberta, False se já tiver sido encerrada

    hospede = relationship("Hospede", back_populates="hospedagens")
    quarto = relationship("Quarto", back_populates="hospedagens")
    despesas = relationship("Despesa", back_populates="hospedagem", cascade="all, delete-orphan")


class Hospede(Base):
    __tablename__ = 'hospedes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    cpf = Column(String, unique=True)
    telefone = Column(String)
    endereco = Column(String)  # 'Estado [PI], cidade [Picos]'
    empresa = Column(String, default="------")

    hospedagens = relationship("Hospedagem", back_populates="hospede")


class Quarto(Base):
    __tablename__ = 'quartos'
    numero = Column(Integer, primary_key=True)
    tipo = Column(String)
    disponivel = Column(Boolean)

    hospedagens = relationship("Hospedagem", back_populates="quarto")


class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String, unique=True)
    senha = Column(String)
    tipo = Column(String)


class Despesa(Base):
    __tablename__ = 'despesas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_hospedagem = Column(Integer, ForeignKey('hospedagens.id'), nullable=False)
    id_produto = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_produto = Column(Float, nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(DateTime, default=datetime.datetime.now)

    hospedagem = relationship("Hospedagem", back_populates="despesas")
    produto = relationship("Produto", back_populates="despesas")
    

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)

    despesas = relationship("Despesa", back_populates="produto")


# Função para iniciar o banco
def init_db():
    """Cria as tabelas no banco de dados se não existirem."""
    Base.metadata.create_all(bind=db)
    print("Banco de dados inicializado/verificado.")


if __name__ == "__main__":
    print("Inicializando o banco de dados...")
    init_db()
    print("Processo concluído.")
