from models.models import Usuario, db, Session

def login(usuario, senha):
    with Session as session:
        try:
            usuario_encontrado = session.query(Usuario).filter_by(usuario=usuario, senha=senha).first()
            if usuario_encontrado:
                return usuario_encontrado
            else:
                return None
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None 