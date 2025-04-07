from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

db = create_engine('sqlite:///data/hp-prime.db')
Base = declarative_base()
Session = sessionmaker(bind=db)

class Hospede(Base):
    __tablename__ = 'hospedes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    cpf = Column(String, unique=True)
    telefone = Column(String)
    endereco = Column(String) #'Estado [PI], cidade[Picos]'
    empresa = Column(String, default="------")
    
    hospedagens = relationship("Hospedagem", backref="hospede")
    relatorios = relationship("Relatorio", backref="hospede")

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

    hospedagens = relationship("Hospedagem", backref="quarto")
    relatorios = relationship("Relatorio", backref="quarto")

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String, unique=True)
    senha = Column(String)
    tipo = Column(String)
    

class Hospedagem(Base):
    __tablename__ = 'hospedagems'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_hospede = Column(String, ForeignKey('hospedes.cpf'))
    id_quarto = Column(Integer, ForeignKey('quartos.numero'))
    data_entrada = Column(DateTime, default=datetime.datetime.now())
    data_saida = Column(DateTime)
    qtd_hospedes = Column(Integer)
    valor_diaria = Column(Integer)

class Relatorio(Base):
    __tablename__ = 'relatorios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_hospede = Column(String, ForeignKey('hospedes.cpf'))
    id_quarto = Column(Integer, ForeignKey('quartos.numero'))
    data_entrada = Column(DateTime, default=datetime.datetime.now())
    data_saida = Column(DateTime)
    qtd_hospedes = Column(Integer)
    valor_diaria = Column(Integer)

# class Reserva(Base):
#     __tablename__ = 'reservar'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     id_hospede = Column(Integer, ForeignKey('hospedes.cpf'))
#     id_quarto = Column(Integer, ForeignKey('quartos.numero'))
#     data_entrada = Column(Datetime)
#     data_saida = Column(Datetime)
#     qtd_hospedes = Column(Integer)
#     valor_diaria = Column(Integer)
#     observacao = Column(String)

# class Produto(Base):
# class Despesa(Base): 

def init_db():
    """Cria as tabelas no banco de dados se não existirem."""
    Base.metadata.create_all(bind=db)
    print("Banco de dados inicializado/verificado.")

if __name__ == "__main__":
    # Se executar este script diretamente, cria o DB
    print("Inicializando o banco de dados...")
    init_db()
    print("Processo concluído.")
