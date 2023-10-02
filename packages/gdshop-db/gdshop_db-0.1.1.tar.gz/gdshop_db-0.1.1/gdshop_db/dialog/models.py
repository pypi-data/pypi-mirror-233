from gdshop_db.db import BaseTable, mapper_registry


@mapper_registry.mapped
class Dialogs(BaseTable):
    __tablename__ = "dialog_dialogs"

    ...


@mapper_registry.mapped
class Message(BaseTable):
    __tablename__ = "dialog_messages"

    ...
