from typing import List

from app.services.investing import investing_process
from app.api.validators import (check_charity_project_active,
                            check_charity_project_update,
                            check_charity_project_was_invested,
                            check_name_duplicate,
                            check_project_before_edit)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                     CharityProjectDB,
                                     CharityProjectUpdate)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Создает благотворительный проект.
    """
    await check_name_duplicate(charity_project.name, session)
    project_id = await charity_project_crud.get_project_id_by_name(
        charity_project.name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект уже существует!'
        )
    new_project = await charity_project_crud.create(charity_project, session)
    await investing_process(new_project, Donation, session)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех проектов."""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await check_project_before_edit(
        charity_project_id, session
    )
    project = await check_charity_project_active(project, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_charity_project_update(
            charity_project_id, session, obj_in.full_amount)
    project = await charity_project_crud.update(
        db_obj=project,
        obj_in=obj_in,
        session=session
    )
    project = await investing_process(project, Donation, session)
    return project

@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_meeting_room(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Удаляет проект. Нельзя удалить проект,
    в который уже были инвестированы средства, его можно только закрыть.
    """
    charity_project = await check_project_before_edit(
        charity_project_id, session
    )
    check_charity_project_was_invested(project)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
