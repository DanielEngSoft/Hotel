from operations.hospedes_operations  import cadastrar_hospede, listar_hospedes, atualizar_hospede, excluir_hospede
from operations.funcionarios_operations import cadastrar_funcionario, listar_funcionarios, atualizar_funcionario, excluir_funcionario
from operations.quartos_operations import cadastrar_quarto, listar_quartos,listar_quartos_disponiveis, listar_quartos_ocupados, atualiza_tipo, excluir_quarto
from operations.usuarios_operations import criar_usuario, listar_usuarios, atualizar_usuario, excluir_usuario
from operations.hospedagem_operations import abrir_hospedagem, listar_hospedagens, fechar_hospedagem
from operations.relatorios_operations import relatorio_hospedagem, relatorio_hospedes
from views.menus_para_terminal import menu_principal, menu_usuarios, menu_quartos, menu_hospedar, menu_hospedes, menu_funcionarios, menu_relatorios

from os import system

if __name__ == "__main__":
    while True:
        system('cls')
        opcao = menu_principal()
        if opcao == "1": # Hospedagem
            while True:
                system('cls')
                opcao_hospedagem = menu_hospedar()
                if opcao_hospedagem == "1": # Abri hospegadem
                    abrir_hospedagem()
                elif opcao_hospedagem == "2": # Listar hospedagem
                    listar_hospedagens()
                elif opcao_hospedagem == "3": # Fechar hospedagem
                    fechar_hospedagem()
                elif opcao_hospedagem == "0":
                    break
                else:
                    print("Opção inválida. Tente novamente.")

                system('pause')
                system('cls')

        elif opcao == "2": # Quartos
            while True:
                system('cls')
                opcao_quarto = menu_quartos()
                if opcao_quarto == "1": # Cadastrar quarto
                    cadastrar_quarto()
                elif opcao_quarto == "2": # Listar quartos
                    listar_quartos()
                elif opcao_quarto == "3": # Listar quartos disponíveis
                    listar_quartos_disponiveis()
                elif opcao_quarto == "4": # Listar quartos ocupados
                    listar_quartos_ocupados()
                elif opcao_quarto == "5": # Atualizar tipo de quarto
                    atualiza_tipo()
                elif opcao_quarto == "6": # Excluir quarto
                    excluir_quarto()
                # elif opcao_quarto == "7": # Atualizar status do quarto
                #     atualiza_status()
                elif opcao_quarto == "0":
                    break
                else:
                    print("Opção inválida. Tente novamente.")

                system('pause')
                system('cls')

        elif opcao == "3": # Hospedes
            while True:
                system('cls')
                opcao_hospede = menu_hospedes()
                if opcao_hospede == "1": # Cadastrar hóspede
                    cadastrar_hospede()
                elif opcao_hospede == "2": # Listar hóspedes
                    listar_hospedes()
                elif opcao_hospede == "3": # Atualizar hóspede
                    atualizar_hospede()
                elif opcao_hospede == "4": # Excluir hóspede
                    excluir_hospede()
                elif opcao_hospede == "0":
                    break
                else:
                    print("Opção inválida. Tente novamente.")

                system('pause')
                system('cls')
                

        elif opcao == "4": # Funcionários
            while True:
                system('cls')
                opcao_funcionario = menu_funcionarios()
                if opcao_funcionario == "1": # Cadastrar funcionário
                    cadastrar_funcionario()
                elif opcao_funcionario == "2": # Listar funcionários
                    listar_funcionarios()
                elif opcao_funcionario == "3": # Atualizar funcionário
                    atualizar_funcionario()
                elif  opcao_funcionario == "4": # Excluir funcionário
                    excluir_funcionario()
                elif opcao_funcionario == "0":
                    break
                else:
                    print("Opção inválida. Tente novamente.")
                    
                system('pause')
                system('cls')

        elif opcao == "5": # Usuários
            while True:
                system('cls')
                opcao_usuario = menu_usuarios()
                if opcao_usuario == "1": # Cadastrar usuário
                    criar_usuario()
                elif opcao_usuario == "2": # Listar usuários
                    listar_usuarios()
                elif opcao_usuario == "3": # Atualizar usuário
                    atualizar_usuario
                elif opcao_usuario == "4": # Excluir usuário
                    excluir_usuario()
                elif opcao_usuario == "0":
                    break
                else:
                    print("Opção inválida. Tente novamente.")
                
                system('pause')
                system('cls')
        elif opcao == "6": # Relatórios
            while True:
                system('cls')
                opcao_usuario = menu_relatorios()
                if opcao_usuario == "1": # Relatório de hospedagem
                    relatorio_hospedagem()
                elif opcao_usuario == "2": # Relatório de hóspedes
                    relatorio_hospedes()
                elif opcao_usuario == "3": # Relatório Diário
                    pass
                elif opcao_usuario == "0":
                    break
                else:
                    print("Opção inválida. Tente novamente.")
                
                system('pause')
                system('cls')

        elif opcao == "0":
            system('cls')
            print('Volte sempre!')        
            break
        else:
            print("Opção inválida. Tente novamente.")
            system('pause')
            system('cls')
        