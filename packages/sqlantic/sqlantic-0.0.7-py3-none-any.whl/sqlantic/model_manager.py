from typing import Container, List, Optional, Type

from pydantic import BaseConfig, BaseModel, create_model


class OrmConfig(BaseConfig):
    from_attributes = True


class ModelManager:
    def __init__(self):
        self.models = {}
        self.namespaces = {}
        self.namespace_model_base_map = {}

    def add_validator(
        self,
        db_model,
        exclude: Optional[List[str]] = None,
        namespace: Optional[str] = None,
        parent: Optional[str] = None,
    ):
        # ensure directly mapped namespaces do not create
        # recurssive references to base namespace model
        exclude = exclude if exclude is not None else []
        namespace = db_model.__name__ if not namespace else namespace

        self.models[db_model.__name__] = db_model
        new_pydantic_model = self.sqlalchemy_to_pydantic(
            db_model, exclude=exclude, parent=parent
        )

        self.namespaces[namespace] = {db_model.__name__: new_pydantic_model}

        if parent is None:
            self.namespace_model_base_map[namespace] = db_model.__name__

    def refresh_namespaces(self):
        for _, db_model in self.models.items():
            for ns_name, namespace in self.namespaces.items():
                # add non recursive model in each existing namespace
                if db_model.__name__ not in namespace:
                    parent = self.namespace_model_base_map[ns_name]
                    namespace[db_model.__name__] = self.sqlalchemy_to_pydantic(
                        db_model, parent=parent
                    )

    def prepare_model_in_namespace(self, namespace):
        locals().update(self.namespaces[namespace])
        for _, model in self.namespaces[namespace].items():
            model.model_rebuild()

    def prepare_models(self):
        self.refresh_namespaces()
        for ns_name in self.namespaces:
            self.prepare_model_in_namespace(ns_name)

    def sqlalchemy_to_pydantic(
        self, db_model: Type, exclude: Container[str] = [], parent: str = None
    ) -> Type[BaseModel]:
        fields = {}
        validators = {}
        annotations = db_model.__annotations__
        for name, column in annotations.items():
            annot = annotations.get(name)
            if name in exclude:
                continue
            collumn_attr = getattr(db_model, name)

            python_type = annot.__args__[0]
            if hasattr(collumn_attr, "default"):
                default = collumn_attr.default
                if collumn_attr.default is None and not collumn_attr.nullable:
                    default = ...
            else:
                default = ...

            if name not in db_model.__table__.columns:
                # preventing recursive references
                if parent is not None and parent in str(python_type):
                    continue
            fields[name] = (python_type, default)

        pydantic_model = create_model(
            db_model.__name__, __config__=OrmConfig, __validators__=validators, **fields
        )
        pydantic_model.__pydantic_parent_namespace__ = {}

        return pydantic_model
