from models.models import Funcionario, Usuario, db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db)
session = Session()

TIPOS_USUARIOS = ["admin", "padrão"]
def tipo_usuario(tipo):
    while True:    
        if tipo not in TIPOS_USUARIOS:
            print("Tipo de usuário inválido.")
            tipo = input("Digite o tipo de usuário novamente: (admin ou padrão): ")
        else:
            return tipo

def criar_usuario():
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    tipo = input("Tipo de usuário (admin ou padrão): ")
    tipo = tipo_usuario(tipo)
    usuario = Usuario(usuario=usuario, senha=senha, tipo=tipo ) #admin ou padrão
    print("Usuário criado com sucesso!")
    session.add(usuario)
    session.commit()

def  listar_usuarios():
    usuarios = session.query(Usuario).all()
    for usuario in usuarios:
        print(f"ID: {usuario.id}, Usuário: {usuario.usuario}, Tipo: {usuario.tipo}")

def atualizar_usuario():
    usuario = input("Usuário a ser atualizado: ")
    usuario = session.query(Usuario).filter_by(usuario=usuario).first()
    if usuario:
        usuario.senha = input("Nova senha: ")
        usuario.tipo = input("Novo tipo: ")
        usuario.tipo = tipo_usuario(usuario.tipo)
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