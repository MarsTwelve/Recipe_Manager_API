from typing import List
from fastapi import FastAPI, status, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from recipe_manager.recipe import Recipe
from recipe_manager.database.database import Database
from recipe_manager.database.database_validation import (validate_if_document_exists,
                                                         validate_if_update_attr_is_valid)

description = """
Recipe Manager API helps you manage all of your recipes

## Recipes

You will be able to:

**Create Recipes**
**Read Recipes**
**Update Created Recipes**
**Delete Recipes**
"""

app = FastAPI(title="Recipe_Manager_API",
              description=description,
              summary="A recipe manager to manage recipes",
              version="0.7",
              terms_of_service="https://example.com/tos",
              contact={
                  "name": "Matheus S. Fernandes",
                  "url": "https://example.com/contact-us",
                  "email": "matheusfer33@hotmail.com"
              },
              license_info={
                  "name": "General Public Use V3.0",
                  "identifier": "GNU GPL"
              })

metadata_tags = [

]


# Add unity later and change quantity back to float type
class IngredientModel(BaseModel):
    ingredient: str
    quantity: str


class RecipeModel(BaseModel):
    title: str
    description: str | None = Field(default=None, title="Description of the recipe", max_length=200)
    ingredients: List[IngredientModel]
    instructions: str = Field(title="Instructions of the recipe")
    category: str


class UpdateRecipe(BaseModel):
    title: str
    update_attr: str
    update_param: str


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
    if validate_if_document_exists(recipe_dump["title"], session):
        response.status_code = status.HTTP_409_CONFLICT
        return "[WARN]DUPLICATE - This recipe already exists"
    commit = db.sqlalchemy_insert_recipe(recipe_obj, session)
    return commit


@app.get("/recipes", status_code=status.HTTP_200_OK)
def get_recipes(response: Response):
    db = Database()
    session = Session(db.engine)
    result = db.sqlalchemy_select_all(session)
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
