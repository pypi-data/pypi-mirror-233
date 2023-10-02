from gdshop_db.db import BaseTable, mapper_registry


@mapper_registry.mapped
class Documents(BaseTable):
    __tablename__ = "office_documents"

    ...


@mapper_registry.mapped
class Financies(BaseTable):
    __tablename__ = "office_financies"

    ...
