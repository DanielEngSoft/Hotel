def menu_principal():
    print('-' * 30, 'MENU PRINCIPAL', '-' * 30)
    print("1. Hospedagem")
    print("2. Quartos")
    print("3. Hóspedes")
    print("4. Funcionários")
    print("5. Usuários")
    print("6. Relatórios")
    print('-' * 50)
    print("0. Sair")
    print('-' * 50)
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_usuarios():
    print('-' * 30, 'MENU USUÁRIOS', '-' * 30)
    print("1. Cadastrar usuário")
    print("2. Listar usuários")
    print("3. Atualizar usuário")
    print("4. Excluir usuário")
    print('-' * 50)
    print("0. Voltar ao menu principal")
    print('-' * 50)
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_quartos():
    print('-' * 30, 'MENU QUARTOS', '-' * 30)
    print("1. Cadastrar quarto")
    print("2. Listar todos os quartos")
    print("3. Listar quartos disponíveis")
    print("4. Listar quartos ocupados")
    print("5. Atualizar tipo de quarto")
    print("6. Excluir quarto")
    # print("7. Atualizar status do quarto") # Não está sendo utilizado
    print('-' * 50)
    print("0. Voltar ao menu principal")
    print('-' * 50)
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_hospedar():
    print('-' * 30, 'MENU DE HOSPEDAGEM', '-' * 30)
    print("1. Abri hospegadem")
    print("2. Listar hospedagem")
    print("3. Fechar hospedagem")
    print('-' * 50)
    print("0. Voltar ao menu principal")
    print('-' * 50)
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_hospedes():
    print('-' * 30, 'MENU HOSPEDES', '-' * 30)
    print("1. Cadastrar hóspede")
    print("2. Listar hóspedes")
    print("3. Atualizar hóspede")
    print("4. Excluir hóspede")
    print('-' * 50)
    print("0. Voltar ao menu principal")
    print('-' * 50)
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_funcionarios():
    print('-' * 30, 'MENU FUNCIONÁRIOS', '-' * 30)
    print("1. Cadastrar funcionário")
    print("2. Listar funcionários")
    print("3. Atualizar funcionário")
    print("4. Excluir funcionário")
    print('-' * 50)
    print("0. Voltar ao menu principal")
    print('-' * 50)
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_relatorios():
    print('-' * 30, 'MENU RELATORIOS', '-' * 30)
    print("1. Relatorio de hospedagem")
    print("2. Relatorio de clientes")
    print("3. Relatorio diario")
    print('-' * 50)
    print("0. Voltar ao menu principal")
    print('-' * 50)
    opcao = input("Escolha uma opção: ")
    return opcao
