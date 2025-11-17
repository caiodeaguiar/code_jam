from abc import ABC, abstractmethod
from .user import User

class IUserRepository(ABC):
    """
    Define o "contrato" (interface) para o repositório de usuários.
    O resto da aplicação só vai conhecer esta classe.
    """
    
    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        """Busca um usuário pelo username."""
        pass
        
    # @abstractmethod
    # def save(self, user: User):
    #     """Salva um usuário (para criar ou atualizar)."""
    #     pass
