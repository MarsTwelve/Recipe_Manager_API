from sqlalchemy import String, ForeignKey
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from recipe_manager.database.recipe_manager_database_session import engine


class Base(DeclarativeBase):
    pass


class Recipe(Base):
    __tablename__ = "recipe_information"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_title: Mapped[str] = mapped_column(String(50))
    recipe_description: Mapped[str] = mapped_column(String(50))
    recipe_instructions: Mapped[str] = mapped_column(String(450))
    recipe_category: Mapped[str] = mapped_column(String(15))

    ingredients: Mapped[List["Ingredients"]] = relationship(back_populates="recipe")


class Ingredients(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    ingredient: Mapped[str] = mapped_column(String(15))
    quantity: Mapped[str] = mapped_column(String(15))
    recipe_id = mapped_column(ForeignKey("recipe_information.id"))

    recipe: Mapped[Recipe] = relationship(back_populates="ingredients")


Base.metadata.create_all(engine)
