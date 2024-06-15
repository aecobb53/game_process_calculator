from sqlalchemy import create_engine
from game_process_calculator.handlers.base_handler import BaseHandler
from sqlmodel import Session, SQLModel

from .base_handler import BaseHandler

class DatabaseHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        database_url = 'postgres://myuser:mypass@localhost:5430/mydb'
        self.engine = create_engine(database_url)

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        with Session(self.engine) as session:
            yield session
