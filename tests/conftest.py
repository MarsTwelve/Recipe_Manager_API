import pytest
from sqlalchemy.orm import Session
from recipe_manager.Recipe import Recipe
from database.Database import Database


@pytest.fixture
def recipe_with_special_chars():
    recipe_dict = {"title": "      apple           pie       ",
                   "description": "    A    basic     american     apple        pie      ",
                   "instructions": "      BIG      STRING     ",
                   "category": "      grains    ",
                   "ingredients": [{"ingredient": "      apple      ",
                                    "quantity": 1,
                                    "unit": "lb"},
                                   {"ingredient": "   flour    ",
                                    "quantity": 0.55,
                                    "unit": "lb"},
                                   {"ingredient": "  milk  ",
                                    "quantity": 0.55,
                                    "unit": "lb"},
                                   {"ingredient": "  eggs  ",
                                    "quantity": 0.8,
                                    "unit": "lb"}]}
    yield recipe_dict


@pytest.fixture
def create_recipe_object():
    """
    Creates a recipe object using lbs as the measuring unit
    """
    recipe_dict = {"title": "apple pie",
                   "description": "A basic american apple pie",
                   "instructions": "BIG STRING",
                   "category": "grains",
                   "ingredients": [{"ingredient": " apple ",
                                    "quantity": 2,
                                    "unit": "lb"},
                                   {"ingredient": "122 ",
                                    "quantity": 0.55,
                                    "unit": "lb"},
                                   {"ingredient": " pasta ",
                                    "quantity": 0.55,
                                    "unit": "lb"},
                                   {"ingredient": "eggs",
                                    "quantity": 0.8,
                                    "unit": "lb"}]}
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
                                    "quantity": 17.6,
                                    "unit": "oz"},
                                   {"ingredient": "sour cream",
                                    "quantity": 8.8,
                                    "unit": "oz"},
                                   {"ingredient": "cream cheese",
                                    "quantity": 8.8,
                                    "unit": "oz"},
                                   {"ingredient": "milk",
                                    "quantity": 14,
                                    "unit": "oz"}]}
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
def database_empty_instance(database_instance, database_session, scope="session"):
    """
    Creates an empty database instance, uses the "database_instance" and "database_session"
    """

    # Clears database before test function
    database_instance.sqlalchemy_delete_all(database_session)
    yield database_instance

    # Clears database after test function
    database_instance.sqlalchemy_delete_all(database_session)
