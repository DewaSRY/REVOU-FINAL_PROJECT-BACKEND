"""_summary_
Raises:
    Exception: _description_
"""


class DataStoreable[T]:
    """DataStoreable
    Data store able is interface for object receive service of data store service\n
    please : 
        - put the data type generic want to store 
            example `DataStoreable[str]`
        - implement the `get_store` method so the `DataStore` class can store data from the object
    """

    def get_store(self) -> T:  # pylint: disable=undefined-variable
        """get_store
        Raises:
            ValueError: ValueError(f"{self.__class__} not implement get_store")
        Returns:
            TypeObject: object pass ont the interface 
        """
        raise ValueError(f"{self.__class__} not implement get_store")
