from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

# Configuração do banco
db = create_engine('sqlite:///data/hp-prime.db')
Base = declarative_base()
Session = sessionmaker(bind=db)


class Hospede(Base):
    __tablename__ = 'hospedes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    cpf = Column(String, unique=True)
    telefone = Column(String)
    endereco = Column(String)  # 'Estado [PI], cidade [Picos]'
    empresa = Column(String, default="------")

    hospedagens = relationship("Hospedagem", back_populates="hospede")


class Funcionario(Base):
    __tablename__ = 'funcionarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    cpf = Column(String, unique=True)
    telefone = Column(String)


class Quarto(Base):
    __tablename__ = 'quartos'
    numero = Column(Integer, primary_key=True)
    tipo = Column(String)
    disponivel = Column(Boolean)

    hospedagens = relationship("Hospedagem", back_populates="quarto")
    relatorios = relationship("Relatorio", back_populates="quarto")


class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String, unique=True)
    senha = Column(String)
    tipo = Column(String)


class Hospedagem(Base):
    __tablename__ = 'hospedagens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_hospede = Column(String, ForeignKey('hospedes.cpf'))  # CPF como FK (pode trocar por id se quiser)
    id_quarto = Column(Integer, ForeignKey('quartos.numero'))
    data_entrada = Column(DateTime, default=datetime.datetime.now)
    data_saida = Column(DateTime)
    qtd_hospedes = Column(Integer)
    valor_diaria = Column(Float)

    hospede = relationship("Hospede", back_populates="hospedagens")
    quarto = relationship("Quarto", back_populates="hospedagens")


class Relatorio(Base):
    __tablename__ = 'relatorios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_hospede = Column(String, ForeignKey('hospedes.cpf'))
    id_quarto = Column(Integer, ForeignKey('quartos.numero'))
    data_entrada = Column(DateTime, default=datetime.datetime.now)
    data_saida = Column(DateTime)
    qtd_hospedes = Column(Integer)
    valor_diaria = Column(Float)

    quarto = relationship("Quarto", back_populates="relatorios")


# Função para iniciar o banco
def init_db():
    """Cria as tabelas no banco de dados se não existirem."""
    Base.metadata.create_all(bind=db)
    print("Banco de dados inicializado/verificado.")


if __name__ == "__main__":
    print("Inicializando o banco de dados...")
    init_db()
    print("Processo concluído.")
