from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import PositiveInt

from crud.charity_project import charity_project_crud
from models.charity_project import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project

async def check_project_before_edit(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project


async def check_charity_project_active(
    charity_project: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    """Проверяет активный ли проект."""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    return charity_project


async def check_charity_project_update(
    project_id: int,
    session: AsyncSession,
    full_amount_to_update: PositiveInt
):
    """Проверка того, что новая требуемая сумма больше уже внесенной."""
    db_project = await (
        charity_project_crud.get_charity_project_by_id(
            project_id, session
        )
    )
    if db_project.invested_amount > full_amount_to_update:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=(
                'Новая требуемая сумма должна быть больше уже '
                'внесенной в проект суммы'
            )
        )
def check_charity_project_was_invested(
    charity_project: CharityProject,
) -> CharityProject:
    """Проверка на то, что средства уже внесены."""
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
