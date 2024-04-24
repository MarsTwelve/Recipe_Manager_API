from typing import List
from fastapi import FastAPI, status, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from recipe_manager.Recipe import Recipe
from database.Database import Database
from endpoints.post_data_validation import validate_recipe_input
from endpoints.RecipeManagerValidator import RecipeManagerValidator

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
              version="0.7.1",
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
    {
        "name": "post_recipes",
        "description": "Add recipes to the database"
    }
]


class IngredientModel(BaseModel):
    ingredient: str = Field(title="the name of the ingredient", max_length=25)
    quantity: float = Field(title="quantity used in the recipe")
    unit: str = Field(title="the unit the measured ingredient is in", min_length=2, max_length=2)


class RecipeModel(BaseModel):
    title: str = Field(title="The title of the recipe", max_length=25)
    description: str = Field(title="Description of the recipe", max_length=150)
    instructions: str = Field(title="Instructions of the recipe", max_length=500)
    category: str
    ingredients: List[IngredientModel]


class UpdateRecipe(BaseModel):
    title: str = Field(title="the title of the recipe", max_length=25)
    update_attr: str = Field(title="the attribute of the recipe to update", max_length=25)
    update_param: str = Field(title="the actual update parameter", max_length=25)


@app.post("/recipes", status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe: RecipeModel, response: Response):
    recipe_dict = recipe.model_dump()

    if len(recipe_dict["ingredients"]) > 20:
        response.status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        return ("[ERR]LIST_TOO_LONG - You provided a list of ingredients that is too long. "
                "The list of ingredients should have a maximum of 20 ingredients")

    if not recipe_dict["ingredients"]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ("[ERR]EMPTY_LIST - You provided a list of ingredients that is empty. "
                "The list of ingredients should have at least one ingredient")

    validated_recipe = validate_recipe_input(recipe_dict)
    if not isinstance(validated_recipe, dict):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return validated_recipe

    db = Database()
    session = Session(db.engine)

    if RecipeManagerValidator.validate_if_document_exists(validated_recipe["recipe_title"], session):
        response.status_code = status.HTTP_409_CONFLICT
        session.close()
        return "[ERR]DUPLICATE - This recipe already exists."

    recipe_obj = Recipe(validated_recipe["recipe_title"],
                        validated_recipe["recipe_description"],
                        validated_recipe["recipe_category"],
                        validated_recipe["recipe_instructions"])

    recipe_obj.add_ingredients(validated_recipe["ingredients"])

    commit = db.sqlalchemy_insert_recipe(recipe_obj, session)
    session.close()
    return commit


@app.get("/recipes", status_code=status.HTTP_200_OK)
def get_recipes(response: Response):
    db = Database()
    session = Session(db.engine)
    result = db.sqlalchemy_select_all(session)

    try:
        first_item = next(result)

    except StopIteration:
        response.status_code = status.HTTP_204_NO_CONTENT
        session.close()
        return "[ERR]NOT_FOUND - No recipes found on the database."
    session.close()

    return first_item, result


@app.get("/recipes/{recipe_title}", status_code=status.HTTP_200_OK)
def get_recipe_by_title_query(recipe_title_query: str, response: Response):
    valid_query = RecipeManagerValidator(recipe_title_query)
    treated_input = valid_query.space_treatment_validation()

    if not treated_input:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "[ERR]EMPTY_FIELD - Empty fields are not allowed. Please provide a value."

    if valid_query.has_invalid_characters():
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"[ERR]VALIDATION_FAILED - Special characters and digits are not allowed here --> {recipe_title_query}"

    db = Database()
    session = Session(db.engine)

    if not valid_query.validate_if_document_exists(treated_input, session):
        response.status_code = status.HTTP_204_NO_CONTENT
        session.close()
        return "[ERR]NOT_FOUND - The provided recipe does not exist."

    recipe = db.sqlalchemy_select_query_by_title(treated_input, session)
    session.close()
    return recipe


@app.patch("/recipes", status_code=status.HTTP_200_OK)
async def patch_update_recipe(update_recipe: UpdateRecipe, response: Response):
    update_parameters = update_recipe.model_dump()
    treated_update_recipe = {}

    for dict_attr, dict_param in update_parameters.items():
        valid_input = RecipeManagerValidator(dict_param)
        treated_input = valid_input.space_treatment_validation()

        if not treated_input:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return "[ERR]EMPTY_FIELD - Empty fields are not allowed. Please provide a value."

        if valid_input.has_invalid_characters():
            response.status_code = status.HTTP_400_BAD_REQUEST
            return (f"[ERR]VALIDATION_FAILED - Special characters and digits are not allowed here"
                    f" --> {dict_attr}:{dict_param}")

        if dict_attr == "title":
            treated_update_recipe["recipe_title"] = treated_input
            continue

        if dict_attr == "update_param":
            treated_update_recipe["update_param"] = treated_input
            continue

        if dict_attr == "update_attr":
            if not valid_input.has_valid_update_attr():
                response.status_code = status.HTTP_400_BAD_REQUEST
                return "[ERR]INVALID_ATTRIBUTE - This attribute does not exist or doesnt accept update parameters"

            treated_update_recipe["update_attr"] = treated_input

    db = Database()
    session = Session(db.engine)

    if not RecipeManagerValidator.validate_if_document_exists(treated_update_recipe["recipe_title"], session):
        response.status_code = status.HTTP_204_NO_CONTENT
        session.close()
        return "[ERR]NOT_FOUND - The provided recipe does not exist"

    result = db.sqlalchemy_update_recipe_title(treated_update_recipe["recipe_title"],
                                               treated_update_recipe["update_attr"],
                                               treated_update_recipe["update_param"],
                                               session)
    session.close()
    return result


@app.delete("/recipes", status_code=status.HTTP_200_OK)
async def delete_recipe(recipe_title_query: str, response: Response):
    valid_input = RecipeManagerValidator(recipe_title_query)
    treated_input = valid_input.space_treatment_validation()

    if not treated_input:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "[ERR]EMPTY_FIELD - Empty fields are not allowed. Please provide a value."

    if valid_input.has_invalid_characters():
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"[ERR]VALIDATION_FAILED - Special characters and digits are not allowed here --> {recipe_title_query}"

    db = Database()
    session = Session(db.engine)

    if not valid_input.validate_if_document_exists(treated_input, session):
        response.status_code = status.HTTP_204_NO_CONTENT
        session.close()
        return "[ERR]NOT-FOUND - The provided recipe does not exist"

    db.sqlalchemy_delete_recipe(treated_input, session)
    session.close()
    return "The recipe was successfully deleted"
