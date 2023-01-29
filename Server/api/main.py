from fastapi import FastAPI

from .routes import login, account, admin
from .db.access import init_db_access, cleanup_db_access
from .db.models import create_tables


app = FastAPI()

app.include_router(login.ROUTER)
app.include_router(account.ROUTER)
app.include_router(admin.ROUTER)


@app.get('/')
async def welcome():
    return 'Welcome to the Courter API Server'


@app.on_event('startup')
async def on_startup():
    init_db_access(dbms='mysql', db_name='courter_api', echo=True)
    await create_tables()


@app.on_event('shutdown')
async def on_shutdown():
    await cleanup_db_access()
