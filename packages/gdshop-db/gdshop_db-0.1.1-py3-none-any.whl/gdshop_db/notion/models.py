from gdshop_db.db import BaseTable


class NotionBase(BaseTable):
    __abstract__ = True

    # title: list[dict]
    # url: str


class Parent:
    type: str
    block_id: str
    page_id: str


class Property:
    name: str
    content: dict


class Database(NotionBase):
    ...
    # properties: dict[Property]
