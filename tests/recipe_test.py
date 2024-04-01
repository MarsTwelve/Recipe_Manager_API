import pytest
from hamcrest import assert_that, equal_to
from recipe_manager.recipe import Recipe


def test_create_recipe_function():
    recipe_dict = {"title": "apple pie",
                   "description": "A basic american apple pie",
                   "instructions": "BIG STRING",
                   "category": "pie",
                   "ingredients": [{"ingredient": "apple",
                                    "quantity": "3_gr"},
                                   {"ingredient": "flour",
                                    "quantity": "350_gr"},
                                   {"ingredient": "milk",
                                    "quantity": "500_gr"},
                                   {"ingredient": "eggs",
                                    "quantity": "4_gr"}]}
    recipe_obj = Recipe(recipe_dict["title"], recipe_dict["description"], recipe_dict["instructions"],
                        recipe_dict["category"])
    recipe_obj.add_ingredients(recipe_dict["ingredients"])
    assert_that(recipe_obj.show_recipe, equal_to({"recipe_title": "apple pie",
                                                  "recipe_description": "A basic american apple pie",
                                                  "recipe_instructions": "BIG STRING",
                                                  "recipe_category": "pie"}))
