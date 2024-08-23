from fastapi import APIRouter

router = APIRouter(prefix="/sample")


@router.get("/test/")
def test():
    return "Hello world"
