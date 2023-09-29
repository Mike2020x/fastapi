from fastapi import APIRouter

router = APIRouter(
    prefix="/products", tags=["products"], responses={404: {"message": "No encontrado"}}
)  # nice

products_list = ["P1", "P2", "P3", "P4", "P5"]


@router.get("/")
async def products():
    return products_list


@router.get("/{id}")
async def products(id: int):
    return products_list[id]
