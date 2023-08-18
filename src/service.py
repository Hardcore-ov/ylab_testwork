from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.schemas import SchemaBase
from src.submenu.models import Submenu


class BaseService:
    def __init__(self, model):
        self.model = model

    async def get_one(self, obj_id: str, session: AsyncSession):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id))
        return db_obj.scalars().first()

    async def get_many(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(self, obj_in: SchemaBase, session: AsyncSession, id: str | None = None):
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, id=id)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: SchemaBase, obj_in: SchemaBase, session: AsyncSession):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: SchemaBase, session: AsyncSession):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def read_all_subobjects(self, obj_id: str, session: AsyncSession):
        subobjects = await session.execute(
            select(self.model).where(self.model.menu_id == obj_id))
        return subobjects.scalars().all()

    async def create_subobject(self, obj_id: str, obj_in: SchemaBase,
                               session: AsyncSession, id: str | None = None):
        new_data = obj_in.model_dump()
        db_subobj = self.model(**new_data, menu_id=obj_id, id=id)
        session.add(db_subobj)
        await session.commit()
        await session.refresh(db_subobj)
        return db_subobj

    async def create_dish(self, obj_id: str, obj_in: SchemaBase,
                          session: AsyncSession, id: str | None = None):
        new_data = obj_in.model_dump()
        db_subobj = self.model(**new_data, submenu_id=obj_id, id=id)
        session.add(db_subobj)
        await session.commit()
        await session.refresh(db_subobj)
        return db_subobj

    async def read_all_dishes(self, obj_id: str, session: AsyncSession):
        subobjects = await session.execute(
            select(self.model).where(self.model.submenu_id == obj_id))
        subobjects = subobjects.scalars().all()
        return subobjects

    async def read_all_menu(self, session: AsyncSession):
        result = await session.scalars(
            select(self.model).options(
                joinedload(self.model.submenus).joinedload(Submenu.dishes)
            )
        )
        menus = result.unique().all()
        menu_data = jsonable_encoder(menus)
        return menu_data
