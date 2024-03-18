from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from recipe_manager.recipe import Recipe

app = FastAPI()


class IngredientModel(BaseModel):
    ingredient: str
    quantity: float


class RecipeModel(BaseModel):
    title: str
    description: str | None = Field(default=None, title="Description of the recipe", max_length=200)
    ingredients: List[IngredientModel]
    instructions: str = Field(title="Instructions of the recipe")
    category: str


@app.post("/recipes")
async def create_recipe(recipe: RecipeModel):
    recipe_obj = Recipe(recipe.title, recipe.description, recipe.instructions,
                        recipe.category, recipe.ingredients)
    return recipe_obj.create_new_recipe()


@app.get("/recipes")
async def get_recipes():
    return "recipes func goes here"


@app.put("/recipes")
async def update_recipe():
    pass


@app.delete("/recipes")
async def delete_recipe():
    pass
