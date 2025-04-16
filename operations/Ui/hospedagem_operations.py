from models.models import Hospedagem, Quarto, Hospede, Despesa, Session  # Importa os modelos e a conexão com o banco
from sqlalchemy import func
from sqlalchemy.orm import joinedload                           # Utilitários do SQLAlchemy
from sqlalchemy.exc import IntegrityError                       # Para tratar erros de integridade (ex: chaves duplicadas)

from datetime import time, datetime, timedelta

# Função que calcula o valor da diária com base na quantidade de pessoas
def diaria(qtd):
    valores = {1: 100, 2: 150, 3: 200, 4: 250, 5: 350}
    return valores.get(qtd, 350 + max(0, qtd - 5) * 70)


# Função para criar uma nova hospedagem
def create_hospedagem(id_hospede, id_quarto, data_saida, qtd_hospedes, valor_diaria):
    # Inicia uma nova sessão com o banco de dados
    with Session() as session:
        try:
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
                    valor_diaria=valor_diaria
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
    with Session() as session:
        # Consulta todas as hospedagens, carregando também os dados relacionados (quarto e hóspede)
        hospedagens = session.query(Hospedagem)\
            .options(
                joinedload(Hospedagem.quarto),   # Carrega automaticamente os dados do quarto
                joinedload(Hospedagem.hospede)   # Carrega automaticamente os dados do hóspede
            ).all()

        # Retorna a lista de objetos Hospedagem
        return hospedagens
    
def buscar_hospedagem_por_quarto(id_quarto):
    with Session() as session:
        # Busca a hospedagem com base no ID do quarto
        hospedagem = session.query(Hospedagem).filter(Hospedagem.id_quarto == id_quarto, Hospedagem.aberta == True).first()
        if hospedagem:
            return hospedagem
        else:
            print(f"Hospedagem não encontrada para o quarto {id_quarto}.")
            return None

# def hospedagem_com_dados_do_hospede():
#     with Session() as session:
#         query = session.query(Hospedagem).options(
#                     joinedload(Hospedagem.hospede),
#                     joinedload(Hospedagem.quarto)
#                 ).join(Hospede)
#         return query
    
def hospedagens_ativas():
    with Session() as session:
        try:
            # Eager loading dos relacionamentos hospede e quarto
            hospedagens = session.query(Hospedagem).options(joinedload(Hospedagem.hospede), joinedload(Hospedagem.quarto)).filter(Hospedagem.aberta == True).all()
            return hospedagens
        except Exception as e:
            print(f"Erro ao buscar hospedagens ativas: {e}")
            return []
        
def encerrar_hospedagem(id_hospedagem):
    with Session() as session:
        try:
            # Busca a hospedagem com base no ID
            hospedagem = session.query(Hospedagem).filter_by(id=id_hospedagem).first()
            if hospedagem:
                # Atualiza a coluna 'aberta' para False
                hospedagem.aberta = False
                hospedagem.quarto.disponivel = True
                session.commit()
                return True
            else:
                print(f"Hospedagem com ID {id_hospedagem} não encontrada.")
                return False
        except Exception as e:
                print(f"Erro ao encerrar hospedagem: {e}")
                return False
        
def atualiza_diarias():
    now = datetime.now()
    with Session() as session:
        try:
            # Busca todas as hospedagens ativas e ja carrega os dados do hospede e quarto
            hospedagens = session.query(Hospedagem).options(
                joinedload(Hospedagem.hospede),
                joinedload(Hospedagem.quarto)
            ).filter(Hospedagem.aberta.is_(True)).all()

            for hospedagem in hospedagens:
                # Calcula a diferença de dias entre a data de entrada e a data atual
                dias_hospedados = (now.date() - hospedagem.data_entrada.date()).days

                # Verifica se o hóspede já foi hospedado por mais de um dia
                if dias_hospedados > 0:
                    # despesa recebe todas as despesas do hospede
                    despesas = session.query(Despesa).filter_by(
                        id_hospedagem=hospedagem.id
                    ).all()

                    # Percorre as despesas do hóspede
                    for despesa in despesas:
                        # Verifica se o produto é uma diária
                        if despesa.produto and 'DIARIA' in despesa.produto.descricao.upper():
                            # Se a quantidade de diárias é diferente do número de dias hospedados, atualiza a quantidade e o valor
                            if despesa.quantidade != dias_hospedados:
                                despesa.quantidade = dias_hospedados
                                despesa.valor = dias_hospedados * hospedagem.valor_diaria
                                # session.commit() # CASO SEJA NECESSARIO FAZER COMMIT POR HOSPEDAGEM ABERTA

            # Salva as alterações no banco de dados de todas as hospedagens de uma vez. ### ANALIZAR SE É MELHOR ASSIM OU FAZENDO COMIT POR HOSPEDAGEM
            session.commit()

        except Exception as e:
            print(f"Erro ao atualizar diárias: {e}")
            return False
        
def alterar_hospedagem(id_hospedagem, novo_quarto, data_entrada, data_saida):
    with Session() as session:
        try:
            # Busca a hospedagem com base no ID
            hospedagem = session.query(Hospedagem).filter_by(id=id_hospedagem).first()
            if not hospedagem:
                print("Hospedagem não encontrada.")
                return False

            # Busca o novo quarto com base no número
            novo_quarto = session.query(Quarto).filter_by(numero=novo_quarto).first()
            if not novo_quarto:
                print("Quarto não encontrado.")
                return False

            # Atualiza status do quarto atual
            if hospedagem.quarto:
                hospedagem.quarto.disponivel = True

            # Atualiza o quarto da hospedagem
            hospedagem.quarto = novo_quarto
            novo_quarto.disponivel = False

            # Atualiza datas da hospedagem
            hospedagem.data_entrada = data_entrada
            hospedagem.data_saida = data_saida

            # Atualiza data das despesas com "DIÁRIA"
            despesas = session.query(Despesa).filter_by(id_hospedagem=id_hospedagem).all()
            for despesa in despesas:
                if despesa.produto and 'DIARIA' in despesa.produto.descricao.upper():
                    despesa.data = data_entrada

            session.commit()
            return True

        except Exception as e:
            session.rollback()
            print(f"Erro ao alterar hospedagem: {e}")
            return False

        
def total_pessoas_hospedadas():
    with Session() as session:
        try:
            # Soma o total de hóspedes nas hospedagens abertas
            total_pessoas = session.query(func.sum(Hospedagem.qtd_hospedes)).filter_by(aberta=True).scalar()
            return total_pessoas or 0  # Retorna 0 caso o resultado seja None
        except Exception as e:
            print(f"Erro ao calcular total de pessoas hospedadas: {e}")
            return 0

def saidas_amanha():
    with Session() as session:
        try:
            # Define o início e fim do dia de amanhã
            amanha_inicio = datetime.combine(datetime.now().date() + timedelta(days=1), datetime.min.time())
            amanha_fim = datetime.combine(datetime.now().date() + timedelta(days=1), datetime.max.time())

            # Conta as hospedagens abertas com data de saída entre o início e o fim do dia de amanhã
            quantidade = session.query(Hospedagem).filter(
                Hospedagem.aberta.is_(True),
                Hospedagem.data_saida >= amanha_inicio,
                Hospedagem.data_saida <= amanha_fim
            ).count()

            return quantidade
        except Exception as e:
            print(f"Erro ao contar hospedagens com saída amanhã: {e}")
            return 0

