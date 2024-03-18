import pytest
from hamcrest import assert_that, equal_to
from recipe_manager.unit_conversion import UnitConverter


def test_unit_converter_parser_oz():
    ingredients_list = {"ingredient": "pasta",
                        "quantity": "17_oz"}
    unit_converter_obj = UnitConverter(ingredients_list)
    quantity_unit = ingredients_list["quantity"]
    unit_converter_obj.parse_unit(quantity_unit)
    assert_that(unit_converter_obj.unit, equal_to("oz"))


def test_unit_converter_parser_lb():
    ingredients_list = {"ingredient": "pasta",
                        "quantity": "17_lb"}
    unit_converter_obj = UnitConverter(ingredients_list)
    quantity_unit = ingredients_list["quantity"]
    unit_converter_obj.parse_unit(quantity_unit)
    assert_that(unit_converter_obj.unit, equal_to("lb"))


def test_unit_converter_parser_unit_int():
    ingredients_list = {"ingredient": "pasta",
                        "quantity": "4_oz"}
    unit_converter_obj = UnitConverter(ingredients_list)
    quantity_unit = ingredients_list["quantity"]
    unit_converter_obj.parse_unit(quantity_unit)
    assert_that(unit_converter_obj.unit, equal_to("oz"))
    assert_that(unit_converter_obj.quantity, equal_to(4))


def test_unit_converter_parser_unit_float():
    ingredients_list = {"ingredient": "pasta",
                        "quantity": "5.5_oz"}
    unit_converter_obj = UnitConverter(ingredients_list)
    quantity_unit = ingredients_list["quantity"]
    unit_converter_obj.parse_unit(quantity_unit)
    assert_that(unit_converter_obj.unit, equal_to("oz"))
    assert_that(unit_converter_obj.quantity, equal_to(5.5))


def test_unit_converter_convert_unit_from_lb_to_g():
    ingredient_list = [{"ingredient": "pasta",
                        "quantity": "1.1_lb"},
                       {"ingredient": "sour cream",
                        "quantity": "0.55_lb"},
                       {"ingredient": "cream cheese",
                        "quantity": "0.55_lb"},
                       {"ingredient": "milk",
                        "quantity": "0.88_lb"}]
    unit_converter_obj = UnitConverter(ingredient_list)
    unit_converter_obj.get_unit()
    assert_that(unit_converter_obj.converted_units, equal_to([499, 249, 249, 399]))


def test_unit_converter_convert_unit_from_oz_to_g():
    ingredient_list = [{"ingredient": "pasta",
                        "quantity": "17.6_oz"},
                       {"ingredient": "sour cream",
                        "quantity": "8.8_oz"},
                       {"ingredient": "cream cheese",
                        "quantity": "8.8'_oz"},
                       {"ingredient": "milk",
                        "quantity": "14.1_oz"}]
    unit_converter_obj = UnitConverter(ingredient_list)
    unit_converter_obj.get_unit()
    assert_that(unit_converter_obj.converted_units, equal_to([499, 249, 249, 400]))

