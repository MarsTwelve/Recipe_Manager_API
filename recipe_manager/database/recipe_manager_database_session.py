from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:password@localhost/recipe_manager", echo=True)
Session = sessionmaker(engine)