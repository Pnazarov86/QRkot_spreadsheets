from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.validators import (validate_charity_project_delete,
                                 validate_charity_project_exists,
                                 validate_charity_project_update)
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def get_charity_project(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Получение проекта."""
    from app.crud.charity_project import charity_project_crud

    project = await charity_project_crud.get(
        charity_project_id, session
    )
    await validate_charity_project_exists(project)
    return project


async def get_project_to_update(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession
) -> CharityProject:
    """Получение проекта для обновления."""
    project = await get_charity_project(
        charity_project_id, session
    )
    await validate_charity_project_update(project, obj_in)
    return project


async def get_project_to_delete(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Получение проекта для удаления."""
    project = await get_charity_project(
        charity_project_id, session
    )
    await validate_charity_project_delete(project)
    return project
