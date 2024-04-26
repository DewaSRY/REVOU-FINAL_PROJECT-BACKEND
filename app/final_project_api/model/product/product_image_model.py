"""_summary_
"""

from .product_image_data import ProductImageData
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, ForeignKey
from app.model_base_service import db, ModelBaseService


class ProductImageModel(
    ProductImageData, ModelBaseService["ProductImageModel"], db.Model
):
    __tablename__ = "product_images"
    id = mapped_column("id", String(36), primary_key=True)
    image_url = mapped_column("image_url", String(50))
    product_id = mapped_column(
        "product_id", String(36), ForeignKey("product.product_id")
    )
