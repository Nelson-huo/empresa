from fastapi import FastAPI

app=FastAPI()

from empresa.auth_roteador import auth_router

from empresa.order_roteador import order_router

app.include_router(auth_router)
app.include_router(order_router)