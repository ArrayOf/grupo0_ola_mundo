from http import HTTPStatus

import aiohttp

from asyncio import sleep

from datetime import datetime
import threading

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from uvicorn import run

app = FastAPI()


class HoraCertaModel(BaseModel):
    hora_certa: datetime = Field(
        default_factory=lambda: datetime.now(),
        description='Informa a hora certa'
    )


@app.get('/')
async def ola_mundo():
    print(f'Thread: {threading.get_native_id()}')
    return 'Olá Mundo!'


@app.get('/hora_certa', response_model=HoraCertaModel, description='Informa a hora certa')
async def hora_certa():
    print(f'Informando a hora certa - Thread: {threading.get_native_id()}')
    await sleep(10)
    return HoraCertaModel()


@app.get('/pagina_web', response_class=HTMLResponse)
def pagina_web():
    return '<html><body><h1>Olá Mundo!</h1></body></html>'


class CEP(BaseModel):
    cep: str = Field(
        description='CEP do lugar'
    )
    uf: str = Field(
        description='UF do lugar'
    )
    cidade: str = Field(
        alias='localidade',
        description='Cidade do lugar'
    )


@app.get('/consulta_cep', response_class=JSONResponse, response_model=CEP)
async def consulta_cep(cep: str = Query(description='CEP a ser consultado')):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://viacep.com.br/ws/{cep}/json/') as response:
            if response.status == HTTPStatus.OK:
                buffer = await response.json()
                return CEP(**buffer)


@app.get('/tela_consulta_cep', response_class=HTMLResponse)
async def tela_consulta_cep():
    return """
        <html>
            <head>
                <title>Consulta CEP</title>
                <link rel="stylesheet" href="https://unpkg.com/missing.css@1.1.1">
            </head>
        
            <body>
                <div> 
                    <h1>Consulta CEP</h1>
                    <form action="/consulta_cep" method="GET">
                        <label>Digite o seu CEP:</label><br>
                        <input type="text" name="cep">
                        <input type="submit" value="Consultar">
                    </form>
                </div>
            </body>
        </html>
    """


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080)
