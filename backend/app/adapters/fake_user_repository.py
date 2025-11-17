from ..domain.user import User
from ..domain.user_repository import IUserRepository

# O seu 'fake_users_db' de main.py agora mora aqui,
# escondido do resto do mundo.
_FAKE_DB_DATA = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$cO6d03oP4TzHWEuJsVaK8Q$e1RbN5x1nieeCs+X8B1LnqCUGSssKiWM2FtqdJJEigA",
        "disabled": False,
    }
}

class FakeUserRepository(IUserRepository):
    """
    Esta é a implementação "fake" do repositório.
    Ela "traduz" (adapta) o dicionário para a nossa Entidade User.
    """
    
    def get_by_username(self, username: str) -> User | None:
        if username not in _FAKE_DB_DATA:
            return None
            
        user_data = _FAKE_DB_DATA[username]
        
        # Converte o dicionário do "banco" para a nossa Entidade de Domínio
        return User(**user_data)
