from fastapi import APIRouter,Depends,HTTPException
from empresa.schemas import FuncionariosSchema,departamentosSchema,ClientesSchema,ProdutosSchema,VendasSchema
from empresa.dependecias import pegar_sessao,verificar_token
from sqlalchemy.orm import Session
from empresa.modelos import Funcionario,Usuario,Departamento,Cliente,Produtos,Venda

order_router=APIRouter(prefix='/auth',tags=['auth'],dependencies=[Depends(verificar_token)])

@order_router.get('/clientes')
async def clientes():
    return {'mensagem': 'clientes'}

@order_router.post('/cadastrar_funcionarios')
async def cadastrar_funcionarios(Funcionarios_schemas:FuncionariosSchema,session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    funcionario_existe=session.query(Funcionario).filter(Funcionario.email==Funcionarios_schemas.email).first()
    if funcionario_existe:
        raise HTTPException(status_code=400,detail='ja existe um funcionario com as mesmas credenciais')
    if not usuarios.admin:
        raise HTTPException(status_code=401,detail='voce nao tem autorizacao para fazer essa operacao')
    novo_funcionario=Funcionario(Funcionarios_schemas.nome,Funcionarios_schemas.email,
    Funcionarios_schemas.telefone,Funcionarios_schemas.endereco,Funcionarios_schemas.salario,Funcionarios_schemas.departamentos_id)
    session.add(novo_funcionario)
    session.commit()
    session.refresh(novo_funcionario)
    return novo_funcionario


@order_router.get('/listar_funcionarios')
async def listar_funcionarios(session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    if not usuarios.admin:
        raise HTTPException(status_code=403, detail='voce nao tem autorizacao para fazer essa operacao')
    funcionarios=session.query(Funcionario).all()
    return funcionarios


@order_router.put('/atualizar_funcionario/{funcionario_id}')
async def atualizar_funcionario(funcionarios_id:int,Funcionarios_schemas:FuncionariosSchema,session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    funcionarios=session.query(Funcionario).filter(Funcionario.id==funcionarios_id).first()
    if not funcionarios:
        raise HTTPException(status_code=400,detail='nao encontrado')
    if not usuarios.admin:
        raise HTTPException(status_code=403,detail='voce nao tem autorizacao para fazer essa operacao')
    funcionarios.nome=Funcionarios_schemas.nome
    funcionarios.email=Funcionarios_schemas.email
    funcionarios.telefone = Funcionarios_schemas.telefone
    funcionarios.endereco = Funcionarios_schemas.endereco
    funcionarios.salario = Funcionarios_schemas.salario
    funcionarios.departamento_id = Funcionarios_schemas.departamentos_id
    session.commit()
    session.refresh(funcionarios)
    return funcionarios

@order_router.patch('/desativar_funcionarios/{funcionario_id}')
async def desativar_funcionario(funcionario_id:int,
                                session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    funcionario=session.query(Funcionario).filter(Funcionario.id==funcionario_id).first()
    if not funcionario:
        raise HTTPException(status_code=404,detail='funcionario nao encontrado')
    if not usuarios.admin:
        raise HTTPException(status_code=403,detail='voce nao tem permissao para fazer esta operacao')
    if not funcionario.ativo:
        raise HTTPException(status_code=400,detail='funcionario ja esta desativado')
    funcionario.ativo=False
    session.commit()
    session.refresh(funcionario)
    return funcionario


@order_router.patch('/ativar_funcionarios/{funcionario_id}')
async def ativar_funcionario(funcionario_id:int,
                                session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    funcionario=session.query(Funcionario).filter(Funcionario.id==funcionario_id).first()
    if not funcionario:
        raise HTTPException(status_code=404,detail='funcionario nao encontrado')
    if not usuarios.admin:
        raise HTTPException(status_code=403,detail='voce nao tem permissao para fazer esta operacao')
    if funcionario.ativo:
        raise HTTPException(status_code=400,detail='funcionario ja esta ativado')
    funcionario.ativo=True
    session.commit()
    session.refresh(funcionario)
    return funcionario

@order_router.post('/cadastro_departamento')
async def cadastro_departamento(departamentos_schemas:departamentosSchema,
                                session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    departamento_existe=session.query(Departamento).filter(Departamento.nome==departamentos_schemas.nome).first()
    if departamento_existe:
        raise HTTPException(status_code=400,detail='ja existe um funcionario com as mesmas credenciais')
    print("id:",usuarios.id,"admin:",usuarios.admin)
    if not usuarios.admin:
        raise HTTPException(status_code=401,detail='voce nao tem autorizacao para fazer essa operacao')
    novo_departamento=Departamento(departamentos_schemas.nome,departamentos_schemas.descricao, departamentos_schemas.responsavel_id)
    session.add(novo_departamento)
    session.commit()
    session.refresh(novo_departamento)
    return {'mensagem:' 'departamento do funcionario  cadastrado com sucesso'}


@order_router.get('/listar_departamentos')
async def listar_departamentos(session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    if not usuarios.admin:
        raise HTTPException(status_code=403, detail='voce nao tem autorizacao para fazer essa operacao')
    departament=session.query(Departamento).all()
    return departament


@order_router.put('/atualizar_departamento/{departamentos_id}')
async def atualizar_departamento(departamentos_id:int,departamentosSchimas:departamentosSchema,session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    departamentoos=session.query(Departamento).filter(Departamento.id==departamentos_id).first()
    if not departamentoos:
        raise HTTPException(status_code=400,detail='nao encontrado')
    if not usuarios.admin:
        raise HTTPException(status_code=403,detail='voce nao tem autorizacao para fazer essa operacao')
    departamentoos.nome=departamentosSchimas.nome
    departamentoos.descricao=departamentosSchimas.descricao
    departamentoos.responsavel_id=departamentosSchimas.responsavel_id

    session.commit()
    session.refresh(departamentoos)
    return departamentoos


@order_router.patch('/desativar_departamento/{departamento_id}')
async def desativar_funcionario(departamento_id:int,
                                session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    departamento=session.query(Departamento).filter(Departamento.id==departamento_id).first()
    if not departamento:
        raise HTTPException(status_code=404,detail='departamento nao encontrado')
    if not usuarios.admin:
        raise HTTPException(status_code=403,detail='voce nao tem permissao para fazer esta operacao')
    if not departamento.ativo:
        raise HTTPException(status_code=400,detail='departamento ja esta desativado')
    departamento.ativo=False
    session.commit()
    session.refresh(departamento)
    return departamento

@order_router.patch('/ativar_departamento/{departamento_id}')
async def ativar_funcionario(departamento_id:int,
                                session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    departamento=session.query(Departamento).filter(Departamento.id==departamento_id).first()
    if not departamento:
        raise HTTPException(status_code=404,detail='departamento nao encontrado')
    if not usuarios.admin:
        raise HTTPException(status_code=403,detail='voce nao tem permissao para fazer esta operacao')
    if departamento.ativo:
        raise HTTPException(status_code=400,detail='departamento ja esta ativado')
    departamento.ativo=True
    session.commit()
    session.refresh(departamento)
    return departamento


@order_router.post('/cadastro_clientes')
async def cadastro_clientes(clientes_schemas:ClientesSchema,
                                session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    cliente=session.query(Cliente).filter(Cliente.email==clientes_schemas.nome).first()
    if cliente:
        raise HTTPException(status_code=400,detail='ja existe um cliente com as mesmas credenciais')
    if not usuarios.admin:
        raise HTTPException(status_code=401,detail='voce nao tem autorizacao para fazer essa operacao')
    novo_cliente=Cliente(clientes_schemas.nome,clientes_schemas.email, clientes_schemas.telefone,clientes_schemas.endereco,clientes_schemas.data_registro)
    session.add(novo_cliente)
    session.commit()
    session.refresh(novo_cliente)
    return {'mensagem:' 'cliente cadastrado com sucesso'}


@order_router.get('/listar_clientes')
async def listar_clientes(session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    if not usuarios.admin:
        raise HTTPException(status_code=403, detail='voce nao tem autorizacao para fazer essa operacao')
    cliente=session.query(Cliente).all()
    return cliente


@order_router.put('/atualizar_dados_clientes/{cliente_id}')
async def atualizar_dados_clientes(cliente_id:int,clientesSchimas:ClientesSchema,session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    cliente=session.query(Cliente).filter(Cliente.id==cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=400,detail='nao encontrado')
    if not usuarios.admin:
        raise HTTPException(status_code=403,detail='voce nao tem autorizacao para fazer essa operacao')
    cliente.nome=clientesSchimas.nome
    cliente.email=clientesSchimas.email
    cliente.telefone=clientesSchimas.telefone
    cliente.endereco=clientesSchimas.endereco
    cliente.data_registro=clientesSchimas.data_registro
    session.commit()
    session.refresh(cliente)
    return cliente


@order_router.post('/cadastro_produtos')
async def cadastro_produtos(produtos_schemas:ProdutosSchema,
                                session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    produto=session.query(Produtos).filter(Produtos.nome==produtos_schemas.nome).first()
    if produto:
        raise HTTPException(status_code=400,detail='ja existe um cliente com as mesmas credenciais')
    if not usuarios.admin:
        raise HTTPException(status_code=401,detail='voce nao tem autorizacao para fazer essa operacao')
    novo_produto=Produtos(produtos_schemas.nome,produtos_schemas.descricao, produtos_schemas.preco,produtos_schemas.quantidade)
    session.add(novo_produto)
    session.commit()
    session.refresh(novo_produto)
    return {'mensagem:' 'novo Produto cadastrado com sucesso'}


@order_router.get('/listar_produtos')
async def listar_produtos(session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    if not usuarios.admin:
        raise HTTPException(status_code=403, detail='voce nao tem autorizacao para fazer essa operacao')
    produto=session.query(Produtos).all()
    return produto

@order_router.put('/atualizar_produtos/{produtos_id}')
async def atualizar_produtos(produto_id:int,produtoSchimas:ProdutosSchema,session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    produto=session.query(Produtos).filter(Produtos.id==produto_id).first()
    if not produto:
        raise HTTPException(status_code=400,detail='nao encontrado')
    if not usuarios.admin:
        raise HTTPException(status_code=403,detail='voce nao tem autorizacao para fazer essa operacao')
    produto.nome=produtoSchimas.nome
    produto.descricao=produtoSchimas.descricao
    produto.preco=produtoSchimas.preco
    produto.quantidade=produtoSchimas.quantidade


    session.commit()
    session.refresh(produto)
    return produto


@order_router.patch('/desativar_produtos/{produtos_id}')
async def desativar_produto(produto_id:int,
                                session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    produto=session.query(Produtos).filter(Produtos.id==produto_id).first()
    if not produto:
        raise HTTPException(status_code=404,detail='produto nao encontrado')
    if not usuarios.admin:
        raise HTTPException(status_code=403,detail='voce nao tem permissao para fazer esta operacao')
    if not produto.ativo:
        raise HTTPException(status_code=400,detail='o produto ja esta desativado')
    produto.ativo=False
    session.commit()
    session.refresh(produto)
    return produto

@order_router.patch('/ativar_produtos/{produtos_id}')
async def ativar_produtos(produto_id:int,
                                session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    produto=session.query(Produtos).filter(Produtos.id==produto_id).first()
    if not produto:
        raise HTTPException(status_code=404,detail='produto nao encontrado')
    if not usuarios.admin:
        raise HTTPException(status_code=403,detail='voce nao tem permissao para fazer esta operacao')
    if produto.ativo:
        raise HTTPException(status_code=400,detail='o produto ja esta ativado')
    produto.ativo=True
    session.commit()
    session.refresh(produto)
    return produto



@order_router.post('/Registro_Vendas')
async def Registro_Vendas(vendas_schemas:VendasSchema,
                                session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    venda=session.query(Venda).filter(Venda.funcionario==vendas_schemas.funcionario).first()
    if venda:
        raise HTTPException(status_code=400,detail='ja existe um cliente com as mesmas credenciais')
    if not usuarios.admin:
        raise HTTPException(status_code=401,detail='voce nao tem autorizacao para fazer essa operacao')
    nova_venda=Venda(vendas_schemas.cliente,vendas_schemas.funcionario, vendas_schemas.data_venda,vendas_schemas.valor_total,vendas_schemas.estado)
    session.add(nova_venda)
    session.commit()
    session.refresh(nova_venda)
    return {'mensagem:' 'nova venda Registrada com sucesso'}


@order_router.get('/listar_Vendas_funcionario')
async def listar_Vendas(session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    if not usuarios.admin:
        raise HTTPException(status_code=403, detail='voce nao tem autorizacao para fazer essa operacao')
    vendas=session.query(Venda).all()
    return vendas


@order_router.put('/atualizar_vendas/{vendas_id}')
async def atualizar_vendas(vendas_id:int,vendasSchimas:VendasSchema,session:Session=Depends(pegar_sessao),usuarios:Usuario=Depends(verificar_token)):
    vendas=session.query(Venda).filter(Venda.id==vendas_id).first()
    if not vendas:
        raise HTTPException(status_code=400,detail='nao encontrado')
    if not usuarios.admin:
        raise HTTPException(status_code=403,detail='voce nao tem autorizacao para fazer essa operacao')
    vendas.cliente=vendasSchimas.cliente
    vendas.funcionario=vendasSchimas.funcionario
    vendas.data_venda=vendasSchimas.data_venda
    vendas.valor_total=vendasSchimas.valor_total
    vendas.estado=vendasSchimas.estado

    session.commit()
    session.refresh(vendas)
    return vendas
