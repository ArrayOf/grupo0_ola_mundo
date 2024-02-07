from datetime import datetime
from time import sleep

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
    return 'Olá Mundo!'


@app.get('/hora_certa', response_model=HoraCertaModel, description='Informa a hora certa')
def hora_certa():
    print(f'Informando a hora certa - {datetime.now().isoformat()}', flush=True)
    sleep(10)
    return HoraCertaModel()


@app.get('/pagina_web', response_class=HTMLResponse)
async def pagina_web():
    return '<html><body><h1>Olá Mundo!</h1></body></html>'


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, workers=1)
