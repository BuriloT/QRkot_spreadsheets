from typing import Optional, List, Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> List[Dict[str, str]]:
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == True # noqa
            )
        )
        projects_list = []
        projects = projects.scalars().all()
        for project in projects:
            projects_list.append({
                'Название проекта': project.name,
                'Время сбора': project.close_date - project.create_date,
                'Описание': project.description
            })
        projects_list = sorted(projects_list, key=lambda k: k['Время сбора'])
        return projects_list


charity_project_crud = CRUDCharityProject(CharityProject)
