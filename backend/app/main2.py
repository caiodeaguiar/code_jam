from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# --- Importações do nosso Domínio, Serviços e Adaptadores ---
from .domain.user_repository import IUserRepository
from .adapters.fake_user_repository import FakeUserRepository
from .services.auth_service import AuthService
from .domain.user import User as UserEntity  # Renomeamos a entidade para evitar colisão
from .domain.user import AuthError, UserNotFound

# --- Constantes de Segurança ---
# (Vieram do seu arquivo original)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Modelos Pydantic (DTOs da API) ---
# (Vieram do seu arquivo original)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    """Este é o Pydantic model, usado para validar a RESPOSTA da API."""
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

# --- Configuração do App FastAPI ---

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especificar seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A URL "tokenUrl" aponta para a *rota* de login abaixo
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Funções de Token (Helpers da API) ---
# (Vieram do seu arquivo original)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Camada de Injeção de Dependência (O "Plumbing" do DDD) ---

def get_user_repo() -> IUserRepository:
    """
    Instancia o repositório. 
    Se quiséssemos mudar para Postgres, SÓ MUDARÍAMOS AQUI.
    """
    return FakeUserRepository()

def get_auth_service(
    repo: IUserRepository = Depends(get_user_repo)
) -> AuthService:
    """Instancia o serviço, injetando o repositório."""
    return AuthService(user_repo=repo)

# --- Funções de Segurança da API (Dependências) ---
# (Refatoradas para usar o Repositório)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    repo: IUserRepository = Depends(get_user_repo)
) -> UserEntity:
    """
    Decodifica o token JWT e busca o usuário NO REPOSITÓRIO.
    Retorna a *Entidade* de Domínio UserEntity.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
        
    # Lógica de "get_user" agora usa o repositório
    user = repo.get_by_username(username=token_data.username)
    
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[UserEntity, Depends(get_current_user)],
):
    """
    Verifica se o usuário (vindo de get_current_user) está ativo.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# --- Rotas da API (Endpoints) ---

@app.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(get_auth_service) # Injeta o serviço
):
    """
    Rota de login. Agora ela é "burra" e só coordena.
    Ela chama o serviço de autenticação.
    """
    try:
        user = auth_service.authenticate(
            form_data.username, form_data.password
        )
    except AuthError as e:
        # Traduz o Erro de Domínio para um Erro HTTP
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect username or password: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Se o serviço retornou, o usuário é válido.
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User) # Responde com o Pydantic Model 'User'
async def read_users_me(
    # Recebe a Entidade 'UserEntity' da função de dependência
    current_user: Annotated[UserEntity, Depends(get_current_active_user)],
):
    """
    Rota protegida que retorna os dados do usuário logado.
    """
    # O FastAPI é inteligente e consegue mapear os atributos da
    # classe UserEntity para o Pydantic model User da resposta.
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[UserEntity, Depends(get_current_active_user)],
):
    """
    Outra rota protegida de exemplo.
    """
    return [{"item_id": "Foo", "owner": current_user.username}]


# --- ROTA DE EXEMPLO (vinda do seu TDD/BDD) ---
# (Não mexe com autenticação, então fica igual)
@app.get("/mod2/{number}")
async def calculate_mod2(number: int):
    """
    Calcula se um número é par ou ímpar (mod 2).
    """
    result = "par" if number % 2 == 0 else "impar"
    return {"number": number, "result": result}
