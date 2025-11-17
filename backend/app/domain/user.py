from pwdlib import PasswordHash
from pydantic import BaseModel # Podemos usar Pydantic para os dados

password_hash = PasswordHash.recommended()

class User:
    """Esta é a nossa Entidade de Domínio."""
    
    def __init__(self, username: str, full_name: str, email: str, hashed_password: str, disabled: bool = False):
        # Validação de regras de negócio pode ir aqui
        if not username:
            raise ValueError("Username é obrigatório")
            
        self.username = username
        self.full_name = full_name
        self.email = email
        self.hashed_password = hashed_password
        self.disabled = disabled

    def verify_password(self, plain_password: str) -> bool:
        """
        O COMPORTAMENTO agora pertence à Entidade.
        O usuário é responsável por verificar sua própria senha.
        """
        return password_hash.verify(plain_password, self.hashed_password)

    @staticmethod
    def create_password_hash(plain_password: str) -> str:
        """Método de fábrica para ajudar a criar um hash"""
        return password_hash.hash(plain_password)

# --- Classes de Erro do Domínio (Opcional, mas boa prática) ---
class AuthError(Exception):
    pass

class UserNotFound(AuthError):
    pass

class InvalidPassword(AuthError):
    pass

class UserInactive(AuthError):
    pass
