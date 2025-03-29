from models.models import Hospede, Hospedagem, Quarto, Relatorio, db
from operations.quartos_operations import listar_quartos_disponiveis, listar_quartos_ocupados
from sqlalchemy.orm import sessionmaker
import datetime

from styles.formatacao_de_entradas import formata_cpf, formata_data
from os import system

Session = sessionmaker(bind=db)
session = Session()

def diaria(pessoas):
    if pessoas == 1:
        return 100
    elif pessoas == 2:
        return 150
    elif pessoas == 3:
        return 200
    elif pessoas == 4:
        return 250
    else:
        return pessoas * 60

def abrir_hospedagem():
    while True:
        if not session.query(Quarto).filter_by(disponivel=True).all():
            system('cls')
            print('-' * 50)
            print("Não há quartos disponíveis.")
            print('-' * 50)
            return

        cpf_hospede = input("CPF do hóspede: ")
        hospede = session.query(Hospede).filter_by(cpf=cpf_hospede).first()
        
        if not hospede:
            print("Hóspede não encontrado.")
            continue

        listar_quartos_disponiveis()
        numero_quarto = str(input("Número do quarto: "))
        quarto = session.query(Quarto).filter_by(numero=numero_quarto).first()
        
        if not quarto:
            while True:
                print("Quarto não encontrado.")
                numero_quarto = input('Digite um quarto disponivel:')                
                quarto = session.query(Quarto).filter_by(numero=numero_quarto).first()
                if quarto:
                    break
                continue
            
        if not quarto.disponivel:
             while True:
                print("Quarto não disponível.")
                numero_quarto = input('Digite um quarto disponivel:')                
                quarto = session.query(Quarto).filter_by(numero=numero_quarto).first()
                if quarto:
                    break
                continue

        data_saida = formata_data(input("Previsão de saída (dd/mm/aaaa): "))
        while True:
            try:
                qtd_hospedes = int(input("Quantidade de hóspedes: "))
                if qtd_hospedes < 1 or qtd_hospedes > 4:
                    print("Quantidade de hóspedes inválida.")
                    continue
                else:
                    break
            except ValueError:
                print("Quantidade de hóspedes inválida.")
                continue

        valor_diaria = diaria(qtd_hospedes)

        hospedagem = Hospedagem(
            id_hospede=hospede.cpf,
            id_quarto=numero_quarto,
            data_saida=data_saida,
            qtd_hospedes=qtd_hospedes,
            valor_diaria=valor_diaria
        )
        
        quarto.disponivel = False
        session.add(hospedagem)
        session.commit()
        print("Hospedagem aberta com sucesso!")
        return hospedagem
def listar_hospedagens():
    system('cls')
    hospedagens = session.query(Hospedagem).all()
    if not hospedagens:
        print("Nenhuma hospedagem encontrada.")
        return
    else:
        for hospedagem in hospedagens:
            hospede = session.query(Hospede).filter_by(cpf=hospedagem.id_hospede).first()
            
            print('-'*50)
            print(f"Número do quarto: {hospedagem.id_quarto}")
            print(f"Hóspede: {hospede.nome}")
            data_entrada = hospedagem.data_entrada.strftime("%d/%m/%Y %H:%M")
            print(f"Data de entrada: {data_entrada}")
            data_saida = hospedagem.data_saida.strftime("%d/%m/%Y")
            print(f"Saída prevista: {data_saida}")
            print(f"Quantidade de hóspedes: {hospedagem.qtd_hospedes}")
            print(f"Valor da diária: {hospedagem.valor_diaria}")
        print('-'*50)


def fechar_hospedagem():
    system('cls')
    hospedagens = session.query(Hospedagem).all()
    if not hospedagens:
        print("Nenhuma hospedagem encontrada.")
        return
    else:
        while True:
            system('cls')
            listar_quartos_ocupados()
            num_quarto = str(input("Número do quarto: "))
            hospedagem = session.query(Hospedagem).filter_by(id_quarto=num_quarto).first()
            if hospedagem:             
                quarto = session.query(Quarto).filter_by(numero=num_quarto).first()
                quarto.disponivel = True
                
                # Gerar relatório...

                hoje = datetime.datetime.now()
                valor_total = hospedagem.valor_diaria * (hoje - hospedagem.data_entrada).days
                if valor_total == 0:
                    valor_total = hospedagem.valor_diaria

                # data_saida_str = datetime.datetime.now()
                # data_saida = datetime.datetime.strftime(data_saida_str,"%d/%m/%Y %H:%M")

                data_entrada_str = hospedagem.data_entrada.strftime("%d/%m/%Y %H:%M")
                data_entrada = datetime.datetime.strptime(data_entrada_str,"%d/%m/%Y %H:%M")

                data_saida_str = datetime.datetime.now()
                data_saida = datetime.datetime.strftime(data_saida_str,"%d/%m/%Y %H:%M")
                data_saida = datetime.datetime.strptime(data_saida,"%d/%m/%Y %H:%M")
                                
                relatorio = Relatorio(id_hospede=hospedagem.id_hospede, id_quarto=hospedagem.id_quarto,data_entrada=data_entrada, data_saida=data_saida, valor_total=valor_total)
                session.add(relatorio)


                session.delete(hospedagem)
                session.commit()
            
                print("Hospedagem fechada com sucesso!")
                break
            else:
                print("Hospedagem não encontrada.")
                system('pause')