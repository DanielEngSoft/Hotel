import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

# --- Início do novo código para caminho dinâmico ---
def get_base_path():
    """
    Determina o caminho base do aplicativo.
    Retorna o diretório temporário do PyInstaller se for um executável,
    caso contrário, retorna o diretório do script atual.
    """
    if getattr(sys, 'frozen', False):
        # Estamos rodando como um executável PyInstaller
        # sys._MEIPASS é o diretório temporário onde o PyInstaller extrai os arquivos
        return sys._MEIPASS
    else:
        # Estamos rodando como um script Python normal
        # Retorna o diretório do script atual
        return os.path.dirname(os.path.abspath(__file__))

# Define o caminho para o arquivo do banco de dados usando a função get_base_path()
# ATENÇÃO: Ajuste a parte ('..', 'data', 'hp-prime.db') conforme a sua estrutura de pastas.
# Exemplos:
# 1. Se 'hp-prime.db' está na mesma pasta do executável/script:
# DATABASE_FILE_PATH = os.path.join(get_base_path(), 'hp-prime.db')
# 2. Se 'hp-prime.db' está na pasta 'data' DENTRO do diretório base:
# DATABASE_FILE_PATH = os.path.join(get_base_path(), 'data', 'hp-prime.db')
# 3. Se 'hp-prime.db' está na pasta 'data' UM NÍVEL ACIMA do diretório base (como no seu código original):
DATABASE_FILE_PATH = os.path.join(get_base_path(), '..', 'data', 'hp-prime.db')

# Imprime o caminho para depuração (útil para verificar se o caminho está correto)
print(f"Tentando conectar ao banco de dados em: {DATABASE_FILE_PATH}")

# A URI do SQLAlchemy agora aponta para o caminho dinâmico
db = create_engine(f'sqlite:///{DATABASE_FILE_PATH}')
# --- Fim do novo código para caminho dinâmico ---


Base = declarative_base()
Session = sessionmaker(bind=db)

# --- Classes de Modelo (mantidas como no seu código original) ---

class Hospedagem(Base):
    __tablename__ = 'hospedagens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_hospede = Column(String, ForeignKey('hospedes.cpf')) 
    id_quarto = Column(Integer, ForeignKey('quartos.numero'))
    data_entrada = Column(DateTime, default=datetime.datetime.now)
    data_saida = Column(DateTime)
    qtd_hospedes = Column(Integer)
    acompanhantes = Column(String)
    valor_diaria = Column(Float)
    obs = Column(String)
    aberta = Column(Boolean, default=True)

    hospede = relationship("Hospede", back_populates="hospedagens")
    quarto = relationship("Quarto", back_populates="hospedagens")
    despesas = relationship("Despesa", back_populates="hospedagem", cascade="all, delete-orphan")

class Reserva(Base):
    __tablename__ = 'reservas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_hospede = Column(String, ForeignKey('hospedes.cpf')) 
    id_quarto = Column(Integer, ForeignKey('quartos.numero'))
    data_entrada = Column(DateTime)
    data_saida = Column(DateTime)
    qtd_hospedes = Column(Integer)
    acompanhantes = Column(String)
    adiantamento = Column(Float, default=0)
    valor_diaria = Column(Float)
    obs = Column(String)

    hospede = relationship("Hospede", back_populates="reservas")
    quarto = relationship("Quarto", back_populates="reservas")

class Hospede(Base):
    __tablename__ = 'hospedes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    cpf = Column(String, unique=True)
    telefone = Column(String)
    endereco = Column(String)
    empresa = Column(String, default="------")

    hospedagens = relationship("Hospedagem", back_populates="hospede")
    reservas = relationship("Reserva", back_populates="hospede")

class Quarto(Base):
    __tablename__ = 'quartos'
    numero = Column(Integer, primary_key=True)
    tipo = Column(String)
    disponivel = Column(Boolean)

    hospedagens = relationship("Hospedagem", back_populates="quarto")
    reservas = relationship("Reserva", back_populates="quarto")

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

class Adiantamento(Base):
    __tablename__ = 'adiantamentos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(DateTime, default=datetime.datetime.now, nullable=False)
    id_hospedagem = Column(Integer, ForeignKey('hospedagens.id'), nullable=False)
    descricao = Column(String, default='PAGAMENTO' ,nullable=False)
    valor = Column(Float, nullable=False)
    metodo_pagamento = Column(String, nullable=False)

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)

    despesas = relationship("Despesa", back_populates="produto")

# --- Função para iniciar o banco ---
def init_db():
    """Cria as tabelas no banco de dados se não existirem."""
    try:
        Base.metadata.create_all(bind=db)
        print("Banco de dados inicializado/verificado com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        print("Por favor, verifique o caminho do arquivo do banco de dados e as permissões.")


if __name__ == "__main__":
    print("Iniciando o processo de inicialização do banco de dados...")
    init_db()
    print("Processo de inicialização do banco de dados concluído.")