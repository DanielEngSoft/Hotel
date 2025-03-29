from models.models import Funcionario, Usuario, db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db)
session = Session()

def criar_usuario():
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    id_funcionario = int(input("ID do funcionário associado: "))
    tipo = input("Tipo de usuário (admin ou padrão): ")

    usuario = Usuario(usuario=usuario, senha=senha, id_funcionario=id_funcionario, tipo=tipo ) #admin ou padrão
    session.add(usuario)
    session.commit()

def  listar_usuarios():
    usuarios = session.query(Usuario).all()
    for usuario in usuarios:
        funcionario = session.query(Funcionario).filter_by(id=usuario.id_funcionario).first()
        print(f"ID: {usuario.id}, Usuário: {usuario.usuario}, Funcionário Associado: {funcionario.nome}, Tipo: {usuario.tipo}")

def atualizar_usuario():
    usuario = input("Usuário a ser atualizado: ")
    usuario = session.query(Usuario).filter_by(usuario=usuario).first()
    if usuario:
        usuario.senha = input("Nova senha: ")
        usuario.tipo = input("Novo tipo: ")
        session.commit()
        print("Usuário atualizado com sucesso!")
    else:
        print("Usuário não encontrado.")


def excluir_usuario():
    usuario = input("Usuário a ser excluído: ")
    usuario = session.query(Usuario).filter_by(usuario=usuario).first()
    if usuario:
        session.delete(usuario)
        session.commit()
        print("Usuário excluído com sucesso!")
    else:
        print("Usuário não encontrado.")