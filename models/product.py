from sqlalchemy import Column, String, Integer  
from sqlalchemy.ext.declarative import declarative_base  

base = declarative_base()

class Product(base):  
  __tablename__ = 'products'

  name = Column(String, primary_key=True)
  calories = Column(Integer)
