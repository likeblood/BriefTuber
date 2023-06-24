from abc import ABC


class ORM(ABC):
    """
    ORM Interface.
    """
    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database: str):
        self._database = database
