from .data_storeable import DataStoreable

# from .data_store_instance import DataStoreInstance


class DataStore:
    "Data Store is some centralizer data on this app"
    USER_TYPE_LIST: list[str] = []

    @classmethod
    def store_user_type(cls, models: list[DataStoreable[str]]):
        "store user type"
        for model in models:
            cls.USER_TYPE_LIST.append(model.get_store())
