from aiogoogle import Aiogoogle
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.crud.validators import check_charity_project_name_duplicate
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)
from app.services.investment import investment
from app.services.utils import (get_charity_project, get_project_to_delete,
                                get_project_to_update)


class CRUDCharityProject(CRUDBase):

    async def create_project(
        self,
        charity_project: CharityProjectCreate,
        session: AsyncSession
    ):
        """Создание проекта."""
        await check_charity_project_name_duplicate(
            charity_project.name, session
        )
        new_project = await self.create(charity_project, session)
        await investment(session, new_project)
        return new_project

    async def partially_update_project(
        self,
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession
    ):
        """Обновление проекта."""
        await get_project_to_update(charity_project_id, obj_in, session)
        if obj_in.name is not None:
            await check_charity_project_name_duplicate(obj_in.name, session)
        return await self.update(
            await get_charity_project(charity_project_id, session),
            obj_in,
            session
        )

    async def get_all_projects(self, session: AsyncSession):
        """Получение всех проектов (Доступно всем)."""
        return await self.get_multi(session)

    async def delete_project(
        self,
        charity_project_id: int,
        session: AsyncSession
    ):
        """Удаление проекта (Только для суперюзеров)."""
        await get_project_to_delete(charity_project_id, session)
        return await self.remove(
            await get_charity_project(charity_project_id, session),
            session
        )

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ):
        """Получение проекта по имени."""
        db_project_id = await session.execute(
            select(self.model.id).where(self.model.name == project_name)
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
        wrapper_services: Aiogoogle
    ) -> list[dict[str, str]]:
        """Получение и сортировка закрытых проектов и генерация отчета."""
        closed_projects = await session.execute(
            select([
                self.model.name,
                (
                    func.julianday(self.model.close_date) -
                    func.julianday(self.model.create_date)
                ).label('collection_time'),
                self.model.description
            ]).where(self.model.fully_invested).order_by('collection_time')
        )
        projects = closed_projects.all()
        spreadsheetid = await spreadsheets_create(wrapper_services)
        await set_user_permissions(spreadsheetid, wrapper_services)
        await spreadsheets_update_value(
            spreadsheetid, projects, wrapper_services
        )
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
