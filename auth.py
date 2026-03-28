from datetime import timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os 
from dotenv import load_dotenv

load_dotenv()

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hashed: str):
    return pwd_context.verify(senha, senha_hashed)

def criar_token_acesso(dados: dict):
    crypted = dados.copy()
    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    crypted["exp"] = expiration
    return jwt.encode(crypted, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token_acesso(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise JWTError("Token inválido")
        return email
    except JWTError as e:
        raise JWTError("Token inválido ou expirado") from e