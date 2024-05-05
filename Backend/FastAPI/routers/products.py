from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["Products"])

# Entity User
class Prod(BaseModel):
    id: str
    name: str
    cost: str

# This is where the db its supposed to be getting the info
prod_list = [Prod(id="P1", name="bracelet", cost="150"),
            Prod(id="P2", name="collar", cost="220"),
            Prod(id="P3", name="doll", cost="85")
         ]

@router.get("/")
async def products():
    return prod_list

@router.get("/{id}")
async def product(id: str):
    return search_prod(id.upper())

def search_prod(id: str):
    product = filter(lambda prod: prod.id == id, prod_list)
    try:
        return list(product)[0]
    except:
        # raise HTTPException(status_code=400, detail="couldnt find user")
        return {"error": "couldnt find product"}