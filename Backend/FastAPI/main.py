from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

### Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
## AUTH Routers
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

@app.get("/")
async def root():
    return "Hola FastApi"

@app.get("/url")
async def url():
    return { "url_curso": "https://mouredev.com/python" }

# Start server: uvicorn main:app --reload
# Api documentation with Swagger: /docs
# Api documentation with redoc: /redoc