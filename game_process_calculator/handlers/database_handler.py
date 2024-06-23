from sqlmodel import Field, SQLModel, Session, create_engine, select
from typing import Optional
import os


class DatabaseHandler:
    def __init__(self):
        self.engine = create_engine(os.getenv("DATABASE_URL"))

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)

    # def get_session(self):
    #     with Session(self.engine) as session:
    #         yield session


# # Define the SQLModel class for the database table
# class Item(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     description: Optional[str] = None
#     price: float
#     quantity: int
#     extra_field: Optional[str] = None

# # # Database connection URL from environment variable
# # DATABASE_URL = os.getenv("DATABASE_URL")

# # # Create the database engine
# # engine = create_engine(DATABASE_URL)

# # # Create the database tables
# # SQLModel.metadata.create_all(engine)

# # CRUD operations
# def create_item(dh, name: str, description: Optional[str], price: float, quantity: int):
#     item = Item(name=name, description=description, price=price, quantity=quantity)
#     # with Session(engine) as session:
#     with Session(dh.engine) as session:
#         session.add(item)
#         session.commit()
#         session.refresh(item)
#         return item

# def read_items(dh, ):
#     # with Session(engine) as session:
#     with Session(dh.engine) as session:
#         statement = select(Item)
#         results = session.exec(statement)
#         return results.all()

# def update_item(dh, item_id: int, name: Optional[str] = None, description: Optional[str] = None, price: Optional[float] = None, quantity: Optional[int] = None):
#     # with Session(engine) as session:
#     with Session(dh.engine) as session:
#         item = session.get(Item, item_id)
#         if not item:
#             return None
#         if name:
#             item.name = name
#         if description:
#             item.description = description
#         if price:
#             item.price = price
#         if quantity:
#             item.quantity = quantity
#         session.add(item)
#         session.commit()
#         session.refresh(item)
#         return item

# def delete_item(dh, item_id: int):
#     # with Session(engine) as session:
#     with Session(dh.engine) as session:
#         item = session.get(Item, item_id)
#         if not item:
#             return None
#         session.delete(item)
#         session.commit()
#         return item

# # Example usage
# # if __name__ == "__main__":
# def init_db():
#     dh = DatabaseHandler()
#     # Create an item
#     new_item = create_item(dh=dh, name="Sample Item", description="This is a sample item", price=10.99, quantity=100)
#     print(f"Created Item: {new_item}")

#     # Read items
#     items = read_items(dh=dh)
#     print(f"Items in database: {items}")

#     # Update an item
#     updated_item = update_item(dh=dh, item_id=new_item.id, price=12.99, quantity=80)
#     print(f"Updated Item: {updated_item}")

#     # # Delete an item
#     # deleted_item = delete_item(dh=dh, new_item.id)
#     # print(f"Deleted Item: {deleted_item}")

#     # # Create an item
#     # new_item = create_item(name="Sample Item", description="This is a sample item", price=10.99, quantity=100)
#     # print(f"Created Item: {new_item}")

#     # # Read items
#     # items = read_items()
#     # print(f"Items in database: {items}")

#     # # Update an item
#     # updated_item = update_item(new_item.id, price=12.99, quantity=80)
#     # print(f"Updated Item: {updated_item}")

#     # # # Delete an item
#     # # deleted_item = delete_item(new_item.id)
#     # # print(f"Deleted Item: {deleted_item}")










# # import os
# # from sqlalchemy import create_engine
# # from sqlmodel import Session, SQLModel

# # from .base_handler import BaseHandler

# # class DatabaseHandler(BaseHandler):
# #     def __init__(self):
# #         super().__init__()
# #         # database_url = 'postgres://myuser:mypass@localhost:5430/mydb'
# #         # database_url = 'postgres://myuser:mypass@localhost:5432/mydb'
# #         # database_url = 'postgresql://myuser:mypass@localhost:5432/postgres'
# #         database_url = 'postgresql://myuser:mypass@localhost:5432/postgres'
# #         # database_url = 'postgresql://myuser:mypass@localhost:5432/mydb'
# #         database_url = "postgresql://postgres:password@localhost:5433/mydb"
# #         # database_url = os.environ['DATABASE_URL']
        
# #         # database_url = 'postgresql://myuser:mypass@localhost:5432/mydb'
# #         # self.engine = create_engine(database_url)
# #         DATABASE_URL = "postgresql://example:example@localhost:5432/example_db"
# #         self.engine = create_engine(DATABASE_URL)

# #     def create_db_and_tables(self):
# #         SQLModel.metadata.create_all(self.engine)

# #     def get_session(self):
# #         with Session(self.engine) as session:
# #             yield session
