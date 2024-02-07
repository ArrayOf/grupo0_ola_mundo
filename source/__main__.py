from asyncio import sleep

from datetime import datetime
import threading

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

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


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080)
