"""_summary_
"""

from .business_data import BusinessDate
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey, String
from app.model_base_service import db, ModelBaseService
from sqlalchemy_utils.types.uuid import UUIDType


class BusinessModel(BusinessDate, ModelBaseService["BusinessModel"], db.Model):
    __tablename__ = "business"
    id = mapped_column("business_id", String(36), primary_key=True)
    user_id = mapped_column("user_id", String(36), ForeignKey("user.user_id"))
    business_name = mapped_column("name", String(50))

    @property
    def business_images(self):
        from .business_image_model import BusinessImageModel

        imagesList = (
            self.session.query(BusinessImageModel)
            .filter(BusinessImageModel.business_id == self.id)
            .all()
        )
        if len(imagesList) == 0:
            return []
        return [img.image_url for img in imagesList]

    @property
    def product(self):
        from app.final_project_api.model.product import ProductModel as PM

        return PM.get_by_business_id(business_id=self.id)

    @property
    def business_types(self):
        from .business_type_model import BusinessTypeModel as BTM

        model: BTM = BTM.get_model_by_id(model_id=self.business_type_id)
        return model.name

    def _set_match_business_type(self, business_type_name: str):
        from .business_type_model import BusinessTypeModel as BT

        businessType = BT.get_match_model_by_name(model_name=business_type_name)
        if businessType == None:
            raise Exception(f"business type : {business_type_name} not found")
        self.business_type_id = businessType.id

    def _get_all_model(self):
        return self.session.query(BusinessModel).all()

    def _get_model_by_id(self, model_id: str) -> "BusinessModel":
        return (
            self.session.query(BusinessModel)
            .filter(BusinessModel.id == model_id)
            .first()
        )

    @classmethod
    def get_by_user_id(cls, user_id: str) -> list["BusinessModel"]:
        return (
            cls.session.query(BusinessModel)
            .filter(BusinessModel.user_id == user_id)
            .all()
        )

    @classmethod
    def add_model(
        cls, user_id: str, business_name: str, business_type_name: str
    ) -> "BusinessModel":
        """_summary_
        Args:
            user_id (str): _description_
            business_name (str): _description_
            business_type_name (str): _description_
        Raises:
            Exception: there is might be because type name not found
        Returns:
            BusinessModel: _description_
        """
        model: BusinessModel
        try:
            model = BusinessModel(
                user_id=user_id,
                business_name=business_name,
                business_type_name=business_type_name,
            )
        except Exception as e:
            raise e
        cls.session.add(model)
        cls.session.commit()
        return model
