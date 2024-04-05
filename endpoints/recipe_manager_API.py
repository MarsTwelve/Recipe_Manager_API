from typing import List
from fastapi import FastAPI, status, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from recipe_manager.recipe import Recipe
from recipe_manager.database.database import Database
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
    db = Database()
    session = Session(db.engine)
    recipe_dump = recipe.model_dump()
    recipe_obj = Recipe(recipe_dump["title"],
                        recipe_dump["description"],
                        recipe_dump["instructions"],
                        recipe_dump["category"])
    recipe_obj.add_ingredients(recipe_dump["ingredients"])
    if validate_if_insert_query_already_exists(recipe_dump["title"]):
        response.status_code = status.HTTP_409_CONFLICT
        return "[WARN]DUPLICATE - This recipe already exists"
    commit = db.sqlalchemy_insert(recipe_obj, recipe_obj.ingredients, session)
    return commit


@app.get("/recipes", status_code=status.HTTP_200_OK)
def get_recipes(response: Response):
    db = Database()
    session = Session(db.engine)
    result = Database.sqlalchemy_select_all(session=session)
    try:
        first_item = next(result)
    except StopIteration:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "[ERR]NOT-FOUND - No recipes found on the database"
    return first_item, result


@app.get("/recipes/{recipe_title}", status_code=status.HTTP_200_OK)
def get_recipe_by_title_query(recipe_title_query: str, response: Response):
    result = sqlalchemy_select_query_by_title(recipe_title_query)
    if result[0] is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "[ERR]NOT-FOUND - The provided recipe does not exist"
    return result


@app.put("/recipes", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def update_recipe():
    pass


@app.delete("/recipes", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def delete_recipe():
    pass
