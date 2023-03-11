from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routes import auth, account, admin, employee, customer, public
from .db.access import cleanup_db_access
from .db.models import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await cleanup_db_access()


APP = FastAPI(lifespan=lifespan)

APP.include_router(auth.ROUTER)
APP.include_router(account.ROUTER)
APP.include_router(admin.ROUTER)
APP.include_router(employee.ROUTER)
APP.include_router(customer.ROUTER)
APP.include_router(public.ROUTER)


@APP.get('/')
async def welcome():
    return 'Welcome to the Courter API Server'
