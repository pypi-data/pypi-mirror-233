from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from sqlorm.model_manager import ModelManager


class Base(DeclarativeBase, AsyncAttrs):
    _orm: ModelManager = ModelManager()

    @classmethod
    def to_pydantic(
        cls,
        exclude: Optional[List[str]] = [],
        namespace: Optional[str] = None,
        parent: Optional[str] = None,
    ):
        def pydantic_mapper(db_model):
            cls._orm.add_validator(
                db_model=db_model, exclude=exclude, namespace=namespace, parent=parent
            )
            return db_model

        return pydantic_mapper

    @classmethod
    def prepare(cls):
        cls._orm.prepare_models()

    def orm(self, namespace: Optional[str] = None):
        model_name = self.__class__.__name__
        namespace = model_name if not namespace else namespace
        return self._orm.namespaces[namespace][model_name].model_validate(self)

    @classmethod
    def model(cls, namespace: Optional[str] = None):
        model_name = cls.__name__
        namespace = model_name if not namespace else namespace
        return cls._orm.namespaces[namespace][model_name]
