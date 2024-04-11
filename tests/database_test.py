import pytest
from hamcrest import assert_that, equal_to
from recipe_manager.exeptions import RecipeNotFoundError


def test_insert_and_read_recipe_db(database_empty_instance, database_session, create_recipe_object_using_oz):
    """"
    Test inserting recipes to the database
    """
    # Calls insert function
    database_empty_instance.sqlalchemy_insert_recipe(create_recipe_object_using_oz,
                                                     database_session)

    # Calls select functions to assert recipe was properly added
    recipe, ingredients = database_empty_instance.sqlalchemy_select_query_by_title("white sauce pasta",
                                                                                   database_session)
    ingredient_list = {}
    for ingredients_test in create_recipe_object_using_oz.ingredients:
        ingredient_list[ingredients_test.ingredient] = ingredients_test.quantity
    assert_that(recipe, equal_to(create_recipe_object_using_oz.show_recipe))
    assert_that(ingredients, equal_to(ingredient_list))


def test_select_all_recipes_db(database_empty_instance, database_session, create_recipe_object_using_oz,
                               create_recipe_object_using_lbs):
    """
    Test selecting a single recipe within the database, using a query parameter
    """
    # Calls insert function for the database
    database_empty_instance.sqlalchemy_insert_recipe(create_recipe_object_using_oz,
                                                     database_session)
    database_empty_instance.sqlalchemy_insert_recipe(create_recipe_object_using_lbs,
                                                     database_session)

    # Calls select all function and uses assert to verify
    recipes = database_empty_instance.sqlalchemy_select_all(database_session)
    recipes_list = []

    for recipe in recipes:
        recipes_list.append(recipe)
    assert_that(len(recipes_list), equal_to(2))
    assert_that(recipes_list[0]["Recipe"], equal_to(create_recipe_object_using_oz.title))
    assert_that(recipes_list[1]["Recipe"], equal_to(create_recipe_object_using_lbs.title))


def test_database_update_recipe_title_db(database_empty_instance, database_session, create_recipe_object_using_lbs):
    """
    Test updating a recipe on the database
    """
    database_empty_instance.sqlalchemy_insert_recipe(create_recipe_object_using_lbs,
                                                     database_session)

    updated_recipe = database_empty_instance.sqlalchemy_update_recipe_title("apple pie",
                                                                            "recipe_title",
                                                                            "cranberry_pie",
                                                                            database_session)

    assert_that(updated_recipe.recipe_title, equal_to("cranberry_pie"))


def test_database_update_recipe_description_db(database_empty_instance, database_session, create_recipe_object_using_lbs):
    """
    Test updating a recipe on the database
    """
    database_empty_instance.sqlalchemy_insert_recipe(create_recipe_object_using_lbs,
                                                     database_session)

    updated_recipe = database_empty_instance.sqlalchemy_update_recipe_title("apple pie",
                                                                            "recipe_description",
                                                                            "new description hah",
                                                                            database_session)

    assert_that(updated_recipe.recipe_description, equal_to("new description hah"))


def test_database_delete_function_db(database_empty_instance, database_session, create_recipe_object_using_oz,
                                     create_recipe_object_using_lbs):
    """
    Test deleting a recipe from the database
    """
    database_empty_instance.sqlalchemy_insert_recipe(create_recipe_object_using_oz,
                                                     database_session)
    database_empty_instance.sqlalchemy_insert_recipe(create_recipe_object_using_lbs,
                                                     database_session)

    database_empty_instance.sqlalchemy_delete_recipe("white sauce pasta", database_session)

    with pytest.raises(RecipeNotFoundError):
        database_empty_instance.sqlalchemy_select_query_by_title("white sauce pasta", database_session)


def test_database_delete_all_function_db(database_empty_instance, database_session, create_recipe_object_using_oz,
                                         create_recipe_object_using_lbs):
    database_empty_instance.sqlalchemy_insert_recipe(create_recipe_object_using_oz,
                                                     database_session)
    database_empty_instance.sqlalchemy_insert_recipe(create_recipe_object_using_lbs,
                                                     database_session)

    database_empty_instance.sqlalchemy_delete_all(database_session)

    recipes = database_empty_instance.sqlalchemy_select_all(database_session)
    recipes_list = []
    for recipe in recipes:
        recipes_list.append(recipe)
    assert_that(len(recipes_list), equal_to(0))
