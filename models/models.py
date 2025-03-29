from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Boolean, DateTime
from sqlalchemy.orm import declarative_base
import datetime

db = create_engine('sqlite:///hp-prime.db')
Base = declarative_base()

class Hospede(Base):
    __tablename__ = 'hospedes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    cpf = Column(String, unique=True)
    telefone = Column(String)

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

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String, unique=True)
    senha = Column(String)
    id_funcionario = Column(Integer, ForeignKey('funcionarios.id'))
    tipo = Column(String)
    

class Hospedagem(Base):
    __tablename__ = 'hospedagems'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_hospede = Column(String, ForeignKey('hospedes.cpf'))
    id_quarto = Column(Integer, ForeignKey('quartos.numero'))
    data_entrada = Column(DateTime, default=datetime.datetime.now())
    data_saida = Column(DateTime) # Corrugir para Date
    qtd_hospedes = Column(Integer)
    valor_diaria = Column(Integer)

class Relatorio(Base):
    __tablename__ = 'relatorios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_hospede = Column(String, ForeignKey('hospedes.cpf'))
    id_quarto = Column(Integer, ForeignKey('quartos.numero'))
    data_entrada = Column(DateTime)
    data_saida = Column(DateTime, default=datetime.datetime.now())
    valor_total = Column(Float)

# class Reserva(Base):
#     __tablename__ = 'reservar'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     id_hospede = Column(Integer, ForeignKey('hospedes.cpf'))
#     id_quarto = Column(Integer, ForeignKey('quartos.numero'))
#     data_entrada = Column(Datetime)
#     data_saida = Column(Datetime)
#     qtd_hospedes = Column(Integer)
#     valor_diaria = Column(Float)

# class Faturar(Base):
    # __tablename__ = 'faturar'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    # id_hospede = Column(Integer, ForeignKey('hospedes.cpf'))
    # id_quarto = Column(Integer, ForeignKey('quartos.numero'))
    # data_entrada = Column(Date)
    # data_saida = Column(Date)
    # valor_total_diarias = Column(Float)
    # valor_total_servicos = Column(Float)
    # valor_total_pagar = Column(Float)

Base.metadata.create_all(db)