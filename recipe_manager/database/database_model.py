from sqlalchemy import String, ForeignKey
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class RecipeModel(Base):
    __tablename__ = "recipe_information"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_title: Mapped[str] = mapped_column(String(50))
    recipe_description: Mapped[str] = mapped_column(String(50))
    recipe_instructions: Mapped[str] = mapped_column(String(450))
    recipe_category: Mapped[str] = mapped_column(String(15))

    ingredients: Mapped[List["IngredientsModel"]] = relationship(back_populates="recipe", cascade="all, delete-orphan")


class IngredientsModel(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    ingredient: Mapped[str] = mapped_column(String(15))
    quantity: Mapped[str] = mapped_column(String(15))
    recipe_id = mapped_column(ForeignKey("recipe_information.id"))

    recipe: Mapped["RecipeModel"] = relationship(back_populates="ingredients")
