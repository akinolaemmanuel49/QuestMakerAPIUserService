from fastapi import FastAPI

from core.api.endpoints.user import users
from core.api.endpoints.role import roles

app = FastAPI()

# Register routers
app.include_router(router=users, tags=['Users'], prefix='/users')
app.include_router(router=roles, tags=['Roles'], prefix='/roles')