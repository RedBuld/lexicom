from contextlib import asynccontextmanager
import redis.asyncio as redis
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import ResponseValidationError
from app_v2 import schemas
from app_v2.routers import BorrowesRequests
from app_v2.routers import BondsRequests
from app_v2.routers import FoldersRequests
from app_v2.routers import UpdatesRequests
from app_v2.routers import ChatsRequests
from app_v2.routers import AuthRequests
from app_v2.routers import MiscRequests
from app_v2.dependencies import update_db

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

RD = redis.Redis( host='localhost', port=6379, db=0, protocol=3, decode_responses=True )

app = FastAPI(
    exception_handlers={
        RequestValidationError: request_validation_error_exception_handler,
        ResponseValidationError: response_validation_error_exception_handler,
        Exception: base_error_exception_handler
    },
    lifespan=lifespan
)
