import pytest
from sqlalchemy.orm import Session
from recipe_manager.recipe import Recipe
from recipe_manager.database.database import Database


@pytest.fixture
def create_recipe_object_using_lbs():
    """
    Creates a recipe object using lbs as the measuring unit
    """
    recipe_dict = {"title": "apple pie",
                   "description": "A basic american apple pie",
                   "instructions": "BIG STRING",
                   "category": "grains",
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
    yield recipe_obj


@pytest.fixture
def create_recipe_object_using_oz():
    recipe_dict = {"title": "white sauce pasta",
                   "description": "A very delicious white sauce pasta",
                   "instructions": "BIG STRING",
                   "category": "grains",
                   "ingredients": [{"ingredient": "pasta",
                                    "quantity": "17.6_oz"},
                                   {"ingredient": "sour cream",
                                    "quantity": "8.8_oz"},
                                   {"ingredient": "cream cheese",
                                    "quantity": "8.8_oz"},
                                   {"ingredient": "milk",
                                    "quantity": "14_oz"}]}
    recipe_obj = Recipe(recipe_dict["title"], recipe_dict["description"], recipe_dict["instructions"],
                        recipe_dict["category"])
    recipe_obj.add_ingredients(recipe_dict["ingredients"])
    yield recipe_obj


@pytest.fixture
def database_instance(scope="session"):
    """
    creates a Database instance
    """
    db = Database()
    yield db


@pytest.fixture
def database_session(database_instance, scope="session"):
    """
    Creates a session, closes session after testing, uses the "database_instance" fixture
    """
    session = Session(database_instance.engine)
    yield session
    session.close()


@pytest.fixture
def database_empty_instance(database_instance, database_session, scope="function"):
    """
    Creates an empty database instance, uses the "database_instance" and "database_session"
    """

    # Clears database before test function
    database_instance.sqlalchemy_delete_all(database_session)
    yield database_instance

    # Clears database after test function
    database_instance.sqlalchemy_delete_all(database_session)