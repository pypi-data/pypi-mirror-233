from sqlalchemy import Column, String

from gdshop_db.db import BaseTable, mapper_registry


@mapper_registry.mapped
class ExchangeRates:
    __tablename__ = "stock_exchangerates"

    currency = Column(String, primary_key=True, index=True)
    # currency: str
    # price: float
    # date: str


@mapper_registry.mapped
class Suppliers(BaseTable):
    __tablename__ = "stock_suppliers"
    ...
    # title: str
    # url: str
    # discount: float
    # vat: float
    # delivery: float


@mapper_registry.mapped
class ShipmentSteps:
    __tablename__ = "stock_shipment_steps"

    key = Column(String, primary_key=True, index=True)
    # key: str
    # title: str
    # description: str


@mapper_registry.mapped
class Shipments(BaseTable):
    __tablename__ = "stock_shipments"
    ...
    # step_key: str
    # exchange_rate_id: str
    # delivery_price: str
    # country: str
    # delivery_plan_date: str
    # delivery_date: str
    # invoice_id: str
    # send_date: str
    # manager_id: str


@mapper_registry.mapped
class ShipmentUnits(BaseTable):
    __tablename__ = "stock_shipment_units"
    ...
    # shipment_id: str
    # original_name: str
    # quantity: int
    # price: str
    # sku_key: str
    # original_sku: str
    # label_image_id: str
    # bearcode: str
    # weight: str
    # size: str


@mapper_registry.mapped
class SKUGroups(BaseTable):
    __tablename__ = "stock_sku_groups"
    ...
    # title: str
    # sku_keys: list[str]


@mapper_registry.mapped
class SKUs:
    __tablename__ = "stock_skus"
    key = Column(String, primary_key=True, index=True)
    # key: str
    # shipment_unit_id: str
    # size_id: str
    # color_id: str
    # brand_id: str
    # category_id: str


@mapper_registry.mapped
class StockSegments(BaseTable):
    __tablename__ = "stock_stock_segments"
    ...
    # title: str
    # category_ids: list[str]
    # product_ids: list[str]


@mapper_registry.mapped
class Products(BaseTable):
    __tablename__ = "stock_products"
    ...
    # name: str
    # description: str
    # material_ids: list[str]
    # details: Optional[list[str]]
    # sku_keys: str
    # seazon_id: str
    # production_video_id: str
    # image_ids: Optional[list[str]]
    # badge_ids: str
    # created_by: str
    # edited_by: str
    # created_time: str
    # last_edited_time: str


@mapper_registry.mapped
class Brands(BaseTable):
    __tablename__ = "stock_brands"
    ...
    # title: str
    # fee: float
    # logo_id: Optional[str]
    # country: str


@mapper_registry.mapped
class Categories(BaseTable):
    __tablename__ = "stock_categories"
    ...
    # title: str
    # fee: float
    # cover_id: str


@mapper_registry.mapped
class Colors(BaseTable):
    __tablename__ = "stock_colors"
    ...
    # title: str
    # sample_id: Optional[str]


@mapper_registry.mapped
class Sizes(BaseTable):
    __tablename__ = "stock_sizes"
    ...
    # title: str
    # description: str
    # brand_id: str
    # category_id: str


@mapper_registry.mapped
class Materials(BaseTable):
    __tablename__ = "stock_materials"
    ...
    # title: str
    # restricts: list[str]
    # advantages: list(str)
    # care: list[str]


@mapper_registry.mapped
class Season(BaseTable):
    __tablename__ = "stock_seasons"
    ...
    # title: str
    # start_date: str
    # end_date: str
