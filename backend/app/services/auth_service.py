from ..domain.user_repository import IUserRepository
from ..domain.user import User, UserNotFound, InvalidPassword, UserInactive

class AuthService:
    """
    Este serviço orquestra o caso de uso "Autenticar Usuário".
    Ele não tem lógica de negócio, apenas coordenação.
    """
    
    def __init__(self, user_repo: IUserRepository):
        # Ele "recebe" o repositório (Injeção de Dependência)
        self.user_repo = user_repo

    def authenticate(self, username: str, password: str) -> User:
        """
        Executa o caso de uso.
        1. Busca o usuário.
        2. Pede ao usuário para verificar a senha.
        3. Verifica se está ativo.
        """
        user = self.user_repo.get_by_username(username)
        
        if not user:
            raise UserNotFound("Usuário não encontrado")
            
        if not user.verify_password(password):
            raise InvalidPassword("Senha incorreta")
            
        if user.disabled:
            raise UserInactive("Usuário inativo")
            
        return user
