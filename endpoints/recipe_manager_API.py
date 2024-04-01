from typing import List
from fastapi import FastAPI, status, Response

from pydantic import BaseModel, Field
from recipe_manager.recipe import Recipe
from recipe_manager.database.recipe_manager_database import (sqlalchemy_insert,
                                                             sqlalchemy_select_all,
                                                             sqlalchemy_select_query_by_title,
                                                             validate_if_insert_query_already_exists)

app = FastAPI()


class IngredientModel(BaseModel):
    ingredient: str
    quantity: str


class RecipeModel(BaseModel):
    title: str
    description: str | None = Field(default=None, title="Description of the recipe", max_length=200)
    ingredients: List[IngredientModel]
    instructions: str = Field(title="Instructions of the recipe")
    category: str


@app.post("/recipes", status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe: RecipeModel, response: Response):
    recipe_dump = recipe.model_dump()
    recipe_obj = Recipe(recipe_dump["title"],
                        recipe_dump["description"],
                        recipe_dump["instructions"],
                        recipe_dump["category"])
    recipe_obj.add_ingredients(recipe_dump["ingredients"])
    if validate_if_insert_query_already_exists(recipe_dump["title"]):
        response.status_code = status.HTTP_409_CONFLICT
        return "[WARN]DUPLICATE - This recipe already exists"
    commit = sqlalchemy_insert(recipe_obj)
    return commit



@app.get("/recipes")
async def get_recipes():
    return "recipes func goes here"


@app.put("/recipes")
async def update_recipe():
    pass


@app.delete("/recipes")
async def delete_recipe():
    pass
