from sqlalchemy.orm import sessionmaker,Session
from fastapi import Depends,HTTPException
from empresa.modelos import db,Usuario
from jose import jwt,JWTError
from empresa.security import SECRET_KEY,ALGORITHM,oauth2_schima



def pegar_sessao():
    try:
     Session=sessionmaker(bind=db)
     session=Session()
     yield session
    finally:
        session.close()



def verificar_token(token:str=Depends(oauth2_schima),session:Session=Depends(pegar_sessao)):
    try:
        dic_info=jwt.decode(token,SECRET_KEY,ALGORITHM)
        id_usuarios=int(dic_info.get('sub'))
    except JWTError:
        raise HTTPException(status_code=401,detail='acesso negado')
    usuarios=session.query(Usuario).filter(Usuario.id==id_usuarios).first()
    if not usuarios:
        raise HTTPException(status_code=400,detail='acesso negado')
    return usuarios

