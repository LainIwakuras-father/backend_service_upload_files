from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/api/assessments", summary="Список заданий для асессора (в зависимости от роли)."
)
async def get_assessments():
    pass


@router.get(
    "/api/assessment{id}", summary="заданиe для асессора (в зависимости от роли)."
)
async def get_assessments():
    pass


@router.get(
    "/api/assessment{id}", summary="заданиe для асессора (в зависимости от роли)."
)
async def get_assessments():
    pass
