from models.models import Hospedagem, Quarto, Hospede, db  # Importa os modelos e a conexão com o banco
from sqlalchemy.orm import sessionmaker, joinedload        # Utilitários do SQLAlchemy
from sqlalchemy.exc import IntegrityError                  # Para tratar erros de integridade (ex: chaves duplicadas)
from models.models import Session as DBSession             # Session já configurada para consultas gerais

# Cria uma fábrica de sessões do banco de dados
Session = sessionmaker(bind=db)

# Função que calcula o valor da diária com base na quantidade de pessoas
def diaria(pessoas):
    valores = {1: 100, 2: 150, 3: 200, 4: 250}  # Preço fixo para até 4 pessoas
    return valores.get(pessoas, pessoas * 60)  # Para mais de 4, cobra R$60 por pessoa

# Função para criar uma nova hospedagem
def create_hospedagem(id_hospede, id_quarto, data_saida, qtd_hospedes):
    try:
        # Inicia uma nova sessão com o banco de dados
        with Session() as session:
            # Busca o quarto com base no número
            quarto = session.query(Quarto).filter_by(numero=id_quarto).first()
            
            # Verifica se o quarto existe e está disponível
            if not quarto or not quarto.disponivel:
                return False

            # Busca o hóspede com base no CPF
            hospede = session.query(Hospede).filter_by(cpf=id_hospede).first()

            # Verifica se o hóspede existe
            if not hospede:
                return False

            # Cria o objeto Hospedagem com os dados fornecidos
            hospedagem = Hospedagem(
                id_hospede=id_hospede,
                id_quarto=id_quarto,
                data_saida=data_saida,
                qtd_hospedes=qtd_hospedes,
                valor_diaria=diaria(qtd_hospedes)
            )

            # Adiciona a nova hospedagem na sessão
            session.add(hospedagem)

            # Atualiza a disponibilidade do quarto para False (ocupado)
            quarto.disponivel = False

            # Salva as alterações no banco
            session.commit()
            return True

    except IntegrityError:
        # Reverte alterações em caso de erro de integridade (ex: duplicidade)
        session.rollback()
        return False
    except Exception as e:
        # Reverte alterações em caso de qualquer outro erro e mostra o erro no console
        session.rollback()
        print(f"Erro ao criar hospedagem: {e}")
        return False

# Função para listar todas as hospedagens registradas no sistema
def listar_hospedagens():
    with DBSession() as session:
        # Consulta todas as hospedagens, carregando também os dados relacionados (quarto e hóspede)
        hospedagens = session.query(Hospedagem)\
            .options(
                joinedload(Hospedagem.quarto),   # Carrega automaticamente os dados do quarto
                joinedload(Hospedagem.hospede)   # Carrega automaticamente os dados do hóspede
            ).all()

        # Retorna a lista de objetos Hospedagem
        return hospedagens
    
def buscar_hospedagem_por_quarto(id_quarto):
    with DBSession() as session:
        # Busca a hospedagem com base no ID do quarto
        hospedagem = session.query(Hospedagem).filter_by(id_quarto=id_quarto).first()
        if hospedagem:
            return hospedagem
        else:
            print(f"Hospedagem não encontrada para o quarto {id_quarto}.")
            return None
