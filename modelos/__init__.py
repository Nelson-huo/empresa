from sqlalchemy import create_engine,Column,String,Integer,Float,Boolean,ForeignKey
from sqlalchemy.orm import declarative_base
from pathlib import Path

db=create_engine('sqlite:///empresa/empresa.db')
print(Path(db.url.database).resolve())

Base=declarative_base()

class Funcionario(Base):
    __tablename__= 'funcionarios'


    id=Column('id',Integer,primary_key=True,autoincrement=True)
    nome=Column('nome',String)
    email=Column('email',String,nullable=False)
    telefone=Column('telefone',Integer)
    endereco=Column('endereco',Integer)
    ativo=Column('ativo',Boolean,default=True)
    salario=Column('salario',Float)
    departamentos_id=Column('departamento',ForeignKey('departamentos.id'))



    def __init__(self,nome,email,telefone,endereco,salario,departamentos_id,ativo=True):
        self.nome=nome
        self.email=email
        self.telefone=telefone
        self.endereco=endereco
        self.ativo = ativo
        self.salario=salario
        self.departamentos_id=departamentos_id

class Departamento(Base):
    __tablename__='departamentos'


    id=Column('id',Integer,primary_key=True,autoincrement=True)
    nome=Column('nome',String)
    descricao=Column('descricao',String)
    responsavel_id=Column(Integer,ForeignKey('funcionarios.id'),nullable=True)
    ativo=Column('ativo',Boolean,default=True)

    def __init__(self,nome,descricao,responsavel_id,ativo=True):
        self.nome=nome
        self.descricao=descricao
        self.responsavel_id=responsavel_id
        self.ativo=ativo


class Cliente(Base):
    __tablename__='clientes'

    id=Column('id',Integer,primary_key=True,autoincrement=True)
    nome=Column('nome',String)
    email=Column('email',String)
    telefone=Column('telefone',Integer)
    endereco=Column('endereco',String)
    data_registro=Column('data_registro',Integer)
    ativo=Column('ativo',Boolean,default=True)

    def __init__(self,nome,email,telefone,endereco,data_registro,ativo=True):
        self.nome=nome
        self.email=email
        self.telefone=telefone
        self.endereco=endereco
        self.data_registro=data_registro
        self.ativo=ativo

class Produtos(Base):
    __tablename__='produtos'

    id=Column('id',Integer,primary_key=True,autoincrement=True)
    nome=Column('nome',String)
    descricao=Column('descricao',String)
    preco=Column('preco',Float)
    quantidade=Column('quantidade',Integer)
    ativo = Column('ativo', Boolean, default=True)



    def __init__(self,nome,descricao,quantidade,preco=0,ativo=True):

        self.nome=nome
        self.descricao=descricao
        self.preco=preco
        self.quantidade=quantidade
        self.ativo =ativo


class Venda(Base):
    __tablename__="vendas"


    id=Column('id',Integer,primary_key=True,autoincrement=True)
    cliente=Column('cliente',ForeignKey('clientes.id'))
    funcionario=Column('funcionario',ForeignKey('funcionarios.id'))
    data_venda=Column('data_venda',Integer)
    valor_total=Column('valor_total',Float)
    estado=Column('estado',String)

    def __init__(self,cliente,funcionario,data_venda,valor_total,estado):

        self.cliente=cliente
        self.funcionario=funcionario
        self.data_venda=data_venda
        self.valor_total=valor_total
        self.estado=estado

class Usuario(Base):
    __tablename__='usuarios'

    id= Column('id',Integer,primary_key=True,autoincrement=True)
    nome=Column('nome',String)
    email=Column('email',String)
    senha=Column('senha',String)
    ativo=Column('ativo',Boolean,default=True)
    admin=Column('admin',Boolean,default=False)

    def __init__(self,nome,email,senha,ativo=True,admin=False):

        self.nome=nome
        self.email=email
        self.senha=senha
        self.ativo=ativo
        self.admin=admin

