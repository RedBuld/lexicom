from contextlib import asynccontextmanager
import redis.asyncio as redis
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import ResponseValidationError
from app import schemas

async def request_validation_error_exception_handler(request: Request, exc: RequestValidationError):
    print(exc)
    validation_errors = exc.errors()
    return JSONResponse(
        status_code=500,
        content={"detail": [str(err) for err in validation_errors]}
    )

async def response_validation_error_exception_handler(request: Request, exc: ResponseValidationError):
    print(exc)
    validation_errors = exc.errors()
    return JSONResponse(
        status_code=500,
        content={"detail": [str(err) for err in validation_errors]}
    )

async def base_error_exception_handler(request: Request, exc: Exception):
    print(exc)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

@asynccontextmanager
async def lifespan( app: FastAPI ):
    yield

RD = redis.Redis( host='redis', port=6379, db=0, protocol=3, decode_responses=True )

app = FastAPI(
    exception_handlers={
        RequestValidationError: request_validation_error_exception_handler,
        ResponseValidationError: response_validation_error_exception_handler,
        Exception: base_error_exception_handler
    },
    lifespan=lifespan
)

@app.get('/check_data', response_model=schemas.DataSchema|None)
async def read(phone: str):
    address = await RD.get(f'address_{phone}')
    if not address:
        return None
    return schemas.DataSchema(phone=phone,address=address)


@app.post('/write_data', response_model=schemas.DataSchema)
async def create_or_update(
    data: schemas.DataSchema
):
    await RD.set(f'address_{data.phone}', data.address)
    address = await RD.get(f'address_{data.phone}')
    return schemas.DataSchema(phone=data.phone,address=address)

# А нужен ли этот endpoint?
# В случа редиса нет необходимости валидации наличия
# таких простых данных для обновления
@app.put('/write_data', response_model=schemas.DataSchema)
async def update(
    data: schemas.DataSchema
):
    await RD.set(f'address_{data.phone}', data.address)
    address = await RD.get(f'address_{data.phone}')
    return schemas.DataSchema(phone=data.phone,address=address)