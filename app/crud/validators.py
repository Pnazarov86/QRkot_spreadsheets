from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import INVESTED_AMOUNT
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_charity_project_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка уникальности имени проекта."""
    from app.crud.charity_project import charity_project_crud
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def validate_charity_project_exists(
        project: CharityProject,
):
    """Проверка существования проекта в базе данных."""
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )


async def validate_charity_project_update(
        project: CharityProject,
        obj_in: CharityProjectUpdate
):
    """Валидация обновления проекта."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )

    if obj_in.full_amount and project.invested_amount > obj_in.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить требуемую сумму меньше уже вложенной!'
        )


async def validate_charity_project_delete(
        charity_project: CharityProject,
):
    """Валидация удаления проекта."""
    if charity_project.invested_amount > INVESTED_AMOUNT:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалить закрытый проект!'
        )
