import datetime
from typing import List, Optional

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gdshop_db.db import BaseTable, mapper_registry
from gdshop_db.marketing.models import Promocodes
from gdshop_db.stock.models import ShipmentUnits


@mapper_registry.mapped
class Orders(BaseTable):
    __tablename__ = "crm_orders"

    manager_id: Mapped[int] = mapped_column(
        ForeignKey("profile_users.phone"), primary_key=True
    )
    max_discount: Mapped[float]
    status: Mapped[str]
    platform_id: Mapped[UUID] = mapped_column(
        ForeignKey("marketing_platforms.id"), primary_key=True
    )  # -
    price: Mapped[float]
    discount: Mapped[int]
    profit: Mapped[float]
    commission: Mapped[float]
    dialog_id: Mapped[UUID] = mapped_column(
        ForeignKey("dialog_dialogs.id"), primary_key=True
    )  # +
    promocode_ids: Mapped[List["Promocodes"]] = relationship(
        back_populates="orders"
    )  # -
    client_id: Mapped[int] = mapped_column(
        ForeignKey("profile_users.phone"), primary_key=True
    )  # +
    shipment_units: Mapped[List["ShipmentUnits"]] = relationship(
        back_populates="orders"
    )
    cart_items: Mapped[List["CartItems"]] = relationship(back_populates="orders")
    burn_rate: Mapped[int]
    error: Mapped[str]
    commit_date: Mapped[datetime.date]
    ad_company_id: Mapped[UUID] = mapped_column(
        ForeignKey("marketing_ads.id"), primary_key=True
    )  # -
    payment_id: Mapped[UUID] = mapped_column(
        ForeignKey("payment_payments.id"), primary_key=True
    )  # -
    delivery_id: Mapped[UUID] = mapped_column(
        ForeignKey("delivery_deliveries.id"), primary_key=True
    )  # -
    created_time: Mapped[datetime.datetime]
    created_by: Mapped[int] = mapped_column(
        ForeignKey("profile_users.phone"), primary_key=True
    )  # +
    last_edited_time: Mapped[datetime.datetime]
    last_edited_by: Mapped[int] = mapped_column(
        ForeignKey("profile_users.phone"), primary_key=True
    )


@mapper_registry.mapped
class CartItems(BaseTable):
    __tablename__ = "crm_cart_items"

    sku_id: Mapped[str] = mapped_column(ForeignKey("stock_skus.key"))  # +
    quantity: Mapped[int]
    price: Mapped[Optional[int]]
