from fastapi import FastAPI

from .routes import login, account, admin, employee, customer, public
from .db.access import cleanup_db_access
from .db.models import create_tables


app = FastAPI()

app.include_router(login.ROUTER)
app.include_router(account.ROUTER)
app.include_router(admin.ROUTER)
app.include_router(employee.ROUTER)
app.include_router(customer.ROUTER)
app.include_router(public.ROUTER)


@app.get('/')
async def welcome():
    return 'Welcome to the Courter API Server'


@app.on_event('startup')
async def on_startup():
    await create_tables()


@app.on_event('shutdown')
async def on_shutdown():
    await cleanup_db_access()
