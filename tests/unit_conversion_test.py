import pytest
from hamcrest import assert_that, equal_to
from recipe_manager.unit_conversion import UnitConverter
from recipe_manager.recipe import Recipe


@pytest.fixture
def create_instance_of_object_recipe_in_lbs():
    recipe_dict = {"title": "apple pie",
                   "description": "A basic american apple pie",
                   "instructions": "BIG STRING",
                   "category": "pie",
                   "ingredients": [{"ingredient": "apple",
                                    "quantity": "1_lb"},
                                   {"ingredient": "flour",
                                    "quantity": "0.55_lb"},
                                   {"ingredient": "milk",
                                    "quantity": "0.55_lb"},
                                   {"ingredient": "eggs",
                                    "quantity": "0.8_lb"}]}
    recipe_obj = Recipe(recipe_dict["title"], recipe_dict["description"], recipe_dict["instructions"],
                        recipe_dict["category"])
    recipe_obj.add_ingredients(recipe_dict["ingredients"])
    return recipe_obj


@pytest.fixture
def create_instance_of_object_recipe_in_oz():
    recipe_dict = {"title": "apple pie",
                   "description": "A basic american apple pie",
                   "instructions": "BIG STRING",
                   "category": "pie",
                   "ingredients": [{"ingredient": "pasta",
                                    "quantity": "17.6_oz"},
                                   {"ingredient": "sour cream",
                                    "quantity": "8.8_oz"},
                                   {"ingredient": "cream cheese",
                                    "quantity": "8.8'_oz"},
                                   {"ingredient": "milk",
                                    "quantity": "14_oz"}]}
    recipe_obj = Recipe(recipe_dict["title"], recipe_dict["description"], recipe_dict["instructions"],
                        recipe_dict["category"])
    recipe_obj.add_ingredients(recipe_dict["ingredients"])
    return recipe_obj


def test_unit_converter_parser_oz(create_instance_of_object_recipe_in_oz):
    unit_converter_obj = UnitConverter(create_instance_of_object_recipe_in_oz.ingredients)
    for ingredient in unit_converter_obj.ingredients_list:
        unit_converter_obj.parse_ingredients_list(ingredient["quantity"])
    assert_that(unit_converter_obj.unit, equal_to(["oz", "oz", "oz", "oz"]))


def test_unit_converter_parser_lb(create_instance_of_object_recipe_in_lbs):
    unit_converter_obj = UnitConverter(create_instance_of_object_recipe_in_lbs.ingredients)
    for ingredient in unit_converter_obj.ingredients_list:
        unit_converter_obj.parse_ingredients_list(ingredient["quantity"])
    assert_that(unit_converter_obj.unit, equal_to(["lb", "lb", "lb", "lb"]))


def test_unit_converter_parser_unit_int(create_instance_of_object_recipe_in_lbs):
    unit_converter_obj = UnitConverter(create_instance_of_object_recipe_in_lbs.ingredients)
    for ingredient in unit_converter_obj.ingredients_list:
        unit_converter_obj.parse_ingredients_list(ingredient["quantity"])
    assert_that(unit_converter_obj.quantity, equal_to([1, 0.55, 0.55, 0.8]))


def test_unit_converter_parser_unit_float(create_instance_of_object_recipe_in_oz):
    unit_converter_obj = UnitConverter(create_instance_of_object_recipe_in_oz.ingredients)
    for ingredient in unit_converter_obj.ingredients_list:
        unit_converter_obj.parse_ingredients_list(ingredient["quantity"])
    assert_that(unit_converter_obj.quantity, equal_to([17.6, 8.8, 8.8, 14]))


def test_unit_converter_convert_unit_from_lb_to_g(create_instance_of_object_recipe_in_lbs):
    unit_converter_obj = UnitConverter(create_instance_of_object_recipe_in_lbs.ingredients)
    unit_converter_obj.get_unit()
    assert_that(unit_converter_obj.convert_pounds_to_grams, equal_to([454, 249, 249, 363]))


def test_unit_converter_convert_unit_from_oz_to_g(create_instance_of_object_recipe_in_oz):
    unit_converter_obj = UnitConverter(create_instance_of_object_recipe_in_oz.ingredients)
    unit_converter_obj.get_unit()
    assert_that(unit_converter_obj.convert_ounces_to_grams, equal_to([499, 249, 249, 397]))
