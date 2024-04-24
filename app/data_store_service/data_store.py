

from .data_storeable import DataStoreable
# from .data_store_instance import DataStoreInstance


class DataStore:
    "Data Store is some centralizer data on this app"
    ACCOUNT_TYPE_LIST: list[str] = []
    TRANSACTION_TYPE_LIST: list[str] = []

    @classmethod
    def store_account_type(cls, models: list[DataStoreable[str]]):  # pylint: disable=unsubscriptable-object
        "store account type "
        for model in models:
            cls.ACCOUNT_TYPE_LIST.append(model.get_store())

    @classmethod
    def store_transaction_type(cls, models: list[DataStoreable[str]]):  # pylint: disable=unsubscriptable-object
        """_summary_

        Args:
            models (list[DataStoreable[str]]): _description_
        """
        for model in models:
            cls.TRANSACTION_TYPE_LIST.append(model.get_store())
