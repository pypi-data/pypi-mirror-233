from gdshop_db.db import BaseTable, mapper_registry


@mapper_registry.mapped
class Images(BaseTable):
    __tablename__ = "content_images"
    ...


@mapper_registry.mapped
class Contents(BaseTable):
    __tablename__ = "content_contents"
    ...


@mapper_registry.mapped
class Files(BaseTable):
    __tablename__ = "content_files"

    ...
