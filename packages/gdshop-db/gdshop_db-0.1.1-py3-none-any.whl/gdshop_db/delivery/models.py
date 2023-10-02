from gdshop_db.db import BaseTable, mapper_registry


@mapper_registry.mapped
class Deliveries(BaseTable):
    __tablename__ = "delivery_deliveries"

    ...
