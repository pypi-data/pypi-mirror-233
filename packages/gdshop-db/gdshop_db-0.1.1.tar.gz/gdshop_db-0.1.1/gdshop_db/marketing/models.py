from gdshop_db.db import BaseTable, mapper_registry


@mapper_registry.mapped
class ADs(BaseTable):
    __tablename__ = "marketing_ads"

    ...


@mapper_registry.mapped
class Promocodes(BaseTable):
    __tablename__ = "marketing_promocodes"

    ...


@mapper_registry.mapped
class Platforms(BaseTable):
    __tablename__ = "marketing_platforms"

    ...


@mapper_registry.mapped
class Posts(BaseTable):
    __tablename__ = "marketing_posts"

    ...


@mapper_registry.mapped
class Pricies(BaseTable):
    __tablename__ = "marketing_pricies"

    ...


@mapper_registry.mapped
class Badges(BaseTable):
    __tablename__ = "marketing_badges"

    ...
    # file_id: str
    # active: bool
    # coordinates: list[str]
    # transparent: str
    # size: str
    # type: str
