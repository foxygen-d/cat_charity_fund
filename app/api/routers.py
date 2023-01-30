from fastapi import APIRouter

from api.endpoints import charity_project_router, donation_router, user_router

main_router = APIRouter()
main_router.include_router(
    charity_project_router, prefix='/charity_project', tags=['charity_projects']
)
main_router.include_router(
    donation_router, prefix='/donation', tags=['donations']
)
main_router.include_router(user_router)
