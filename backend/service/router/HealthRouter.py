from fastapi import APIRouter
from service.constants.Server import ADD_PATH

router = APIRouter(redirect_slashes=False)

@router.get(ADD_PATH)
def read_root():
    return {"Hello": "World"}


