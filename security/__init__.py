from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, oauth2
from dotenv import load_dotenv
import os
from pathlib import Path



load_dotenv(dotenv_path=Path(__file__).resolve().parents[1]/'env')
SECRET_KEY=os.getenv('SECRET_KEY')
ALGORITHM=os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_schima=OAuth2PasswordBearer(tokenUrl='auth/login_form')