from hamcrest import assert_that, equal_to
from recipe_manager.UnitConverter import UnitConverter


def test_unit_converter_parser_lb(create_recipe_object_using_lbs):
    unit_converter_obj = UnitConverter(create_recipe_object_using_lbs.ingredients)
    for ingredient in unit_converter_obj.ingredients_list:
        unit_converter_obj.parse_ingredients_list(ingredient["quantity"])
    assert_that(unit_converter_obj.unit, equal_to(["lb", "lb", "lb", "lb"]))


def test_unit_converter_convert_unit_from_lb_to_g(create_recipe_object_using_lbs):
    unit_converter_obj = UnitConverter(create_recipe_object_using_lbs.ingredients)
    unit_converter_obj.get_unit()
    assert_that(unit_converter_obj.convert_pounds_to_grams, equal_to([454, 249, 249, 363]))


def test_unit_converter_parser_unit_int(create_recipe_object_using_lbs):
    unit_converter_obj = UnitConverter(create_recipe_object_using_lbs.ingredients)
    for ingredient in unit_converter_obj.ingredients_list:
        unit_converter_obj.parse_ingredients_list(ingredient["quantity"])
    assert_that(unit_converter_obj.quantity, equal_to([1, 0.55, 0.55, 0.8]))


def test_unit_converter_parser_oz(create_recipe_object_using_oz):
    unit_converter_obj = UnitConverter(create_recipe_object_using_oz.ingredients)
    for ingredient in unit_converter_obj.ingredients_list:
        unit_converter_obj.parse_ingredients_list(ingredient["quantity"])
    assert_that(unit_converter_obj.unit, equal_to(["oz", "oz", "oz", "oz"]))


def test_unit_converter_parser_unit_float(create_recipe_object_using_oz):
    unit_converter_obj = UnitConverter(create_recipe_object_using_oz.ingredients)
    for ingredient in unit_converter_obj.ingredients_list:
        unit_converter_obj.parse_ingredients_list(ingredient["quantity"])
    assert_that(unit_converter_obj.quantity, equal_to([17.6, 8.8, 8.8, 14]))


def test_unit_converter_convert_unit_from_oz_to_g(create_recipe_object_using_oz):
    unit_converter_obj = UnitConverter(create_recipe_object_using_oz.ingredients)
    unit_converter_obj.get_unit()
    assert_that(unit_converter_obj.convert_ounces_to_grams, equal_to([499, 249, 249, 397]))
