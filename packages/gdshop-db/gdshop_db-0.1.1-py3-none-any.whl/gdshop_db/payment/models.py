from gdshop_db.db import BaseTable, mapper_registry


@mapper_registry.mapped
class Payments(BaseTable):
    __tablename__ = "payment_payments"

    ...
