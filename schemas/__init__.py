from pydantic import BaseModel
from typing import Optional



class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from__attributes=True

class loginSchima(BaseModel):
    email: str
    senha: str

    class Config:
        from__attributes=True


class FuncionariosSchema(BaseModel):

    nome:str
    email:str
    telefone:int
    endereco:str
    ativo:Optional[bool]
    salario:float
    departamentos_id:int

    class Config:
        from__attributes = True

class departamentosSchema(BaseModel):
    nome:str
    descricao:str
    responsavel_id:int
    ativo:Optional[bool]

    class Config:
        from__attributes=True

class ClientesSchema(BaseModel):
    nome:str
    email:str
    telefone:int
    endereco:str
    data_registro:int
    ativo:Optional[bool]

    class Config:
        from__attributes = True


class ProdutosSchema(BaseModel):
    nome:str
    descricao:str
    preco:int
    quantidade:int
    ativo:Optional[bool]


    class Config:
        from__attributes = True

class VendasSchema(BaseModel):
    cliente:int
    funcionario:int
    data_venda:int
    valor_total:float
    estado:str

