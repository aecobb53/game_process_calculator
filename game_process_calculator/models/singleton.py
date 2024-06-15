from datetime import datetime

class ContextSingleton:
    """
    State Singleton for persisting values
    """
    _self = None

    def __new__(cls, logger=None, database=None, config=None, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
            cls._self.logger = logger
            cls._self.database = database
            cls._self.config = config
            cls.time = datetime.now()
        return cls._self

    def add_logger(self, obj):
        print('IN ADD LOGGER')
        print('self')
        print(self)
        print('self.logger')
        print(self.logger)
        print('obj')
        print(obj)
        self.logger = obj

    # def add_config(self, obj):
    #     self.config = obj

    # def add_database(self, obj):
    #     self.database = obj


def create_logger():
    pass

def load_config():
    pass

def connect_to_database():
    pass
