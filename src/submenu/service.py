from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    def __init__(self, model):
        self.model = model

    async def get_one(
        self,
        obj_id: str,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id,
            ),
        )
        return db_obj.scalars().first()

    async def get_many(
        self,
        session: AsyncSession,
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
        self,
        db_obj,
        session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def read_all_subobjects(
        self,
        obj_id: str,
        session: AsyncSession,
    ):
        subobjects = await session.execute(
            select(self.model).where(self.model.menu_id == obj_id),
        )
        return subobjects.scalars().all()

    async def create_subobject(
        self,
        obj_id: str,
        obj_in,
        session: AsyncSession,
    ):
        new_data = obj_in.dict()
        db_subobj = self.model(**new_data, menu_id=obj_id)
        session.add(db_subobj)
        await session.commit()
        await session.refresh(db_subobj)
        return db_subobj

    async def create_dish(
        self,
        obj_id: str,
        obj_in,
        session: AsyncSession,
    ):
        new_data = obj_in.dict()
        db_subobj = self.model(**new_data, submenu_id=obj_id)
        session.add(db_subobj)
        await session.commit()
        await session.refresh(db_subobj)
        return db_subobj

    async def read_all_dishes(
        self,
        obj_id: str,
        session: AsyncSession,
    ):
        subobjects = await session.execute(
            select(self.model).where(self.model.submenu_id == obj_id),
        )
        return subobjects.scalars().all()
