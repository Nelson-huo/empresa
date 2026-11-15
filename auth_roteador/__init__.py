

import jwt
from fastapi import APIRouter,Depends,HTTPException
from empresa.dependecias import pegar_sessao,verificar_token
from empresa.modelos import Usuario
from empresa.security import bcrypt_context
from sqlalchemy.orm import Session
from empresa.schemas import UsuarioSchema,loginSchima
from jose import JWTError
from datetime import datetime,timedelta,timezone
from empresa.security import ALGORITHM,SECRET_KEY,ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm


auth_router=APIRouter(prefix='/auth',tags=['auth'])

def autenticar_token(email,senha,session):
    usuarios=session.query(Usuario).filter(Usuario.email==email).first()
    if not usuarios:
        return False
    elif not bcrypt_context.verify(senha,usuarios.senha):
        return False
    return usuarios

def criar_token(id_usuarios,duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
  data_expiracao=datetime.now(timezone.utc)+duracao_token
  dic_info={'sub':str(id_usuarios),'exp':data_expiracao}
  codificacao_jwt=jwt.encode(dic_info,SECRET_KEY,algorithm=ALGORITHM)
  return codificacao_jwt

def tornar_admin(email,session):
    usuario=session.query(Usuario).filter(Usuario.email=='admin').first()
    if not usuario:
        raise HTTPException(status_code=400,detail='email nao encontrado')
    usuario.admin=True
    session.commit()
    session.refresh(usuario)


@auth_router.get('/')
async def home():
    return {'mensagem': 'bem vindo a rota de pedidos'}

@auth_router.post('/criar_conta')
async def criar_conta(usuario_schemas:UsuarioSchema,session:Session=Depends(pegar_sessao)):
     usuarios=session.query(Usuario).filter(Usuario.email==usuario_schemas.email).first()
     if usuarios:
         raise HTTPException(status_code=400,detail='usuario ja existe')
     senha_cryptografada=bcrypt_context.hash(usuario_schemas.senha)
     novo_usuario=Usuario(usuario_schemas.nome,usuario_schemas.nome,senha_cryptografada)
     session.add(novo_usuario)
     session.commit()
     raise HTTPException(status_code=200, detail=f'novo usuario criado com sucesso {usuario_schemas.email}')

@auth_router.post('/')
async def login(login_schemas:loginSchima,session:Session=Depends(pegar_sessao)):
    usuarios=session.query(Usuario).filter(Usuario.email==login_schemas.email).first()
    if not usuarios:
        raise HTTPException(status_code=400,detail='usuario nao existe, verifique os dados')
    else:
        access_token=criar_token(usuarios.id)
        refresh_token=criar_token(usuarios.id)
        return {'access_token':access_token,
                'refresh_token':refresh_token,
                'token_type': 'bearer'}



@auth_router.post('/login_form')
async def login_form(dados_formulario:OAuth2PasswordRequestForm=Depends(),session:Session=Depends(pegar_sessao)):
    usuarios=autenticar_token(dados_formulario.username,dados_formulario.password,session)
    if not usuarios:
        raise HTTPException(status_code=400,detail='usuario nao existe, verifique os dados')
    else:
        access_token=criar_token(usuarios.id)
        return {'access_token':access_token,
                'token_type': 'bearer'}


@auth_router.get('/refresh')
async def user_refresh_token(usuarios:Usuario=Depends(verificar_token)):
    access_token = criar_token(usuarios.id)
    return {'access_token': access_token,
            'token_type': 'bearer'}
