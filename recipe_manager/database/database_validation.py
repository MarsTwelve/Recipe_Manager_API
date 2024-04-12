"""
SQLAlchemy validation file
"""
from recipe_manager.database.database import RecipeModel, Session
from sqlalchemy import select


def validate_if_document_exists(recipe_title: str, session: Session):
    """
    Validates if the desired document exists in the database
    :param recipe_title: str
        The title of the queried recipe
    :param session: Session
        The database session used to execute the SQL statements
    :return: bool
        Returns a boolean to indicate whether the validation passed or not (might improve to raise exception later)
    """
    select_validate_recipe_stmt = select(RecipeModel).where(RecipeModel.recipe_title == recipe_title)
    validate_result = session.execute(select_validate_recipe_stmt).first()
    if validate_result:
        return True
    return False


def validate_if_update_attr_is_valid(update_attr: str):
    """
    Validates if the attributes passed are valid to update
    :param update_attr: str
        The name of the attribute where the update is to be performed
    :return: bool
        Returns a boolean to indicate whether the validation passed or not (might improve to raise exception later)
    """
    valid_attributes = ["recipe_title", "recipe_description", "recipe_instructions", "recipe_category"]
    if update_attr in valid_attributes:
        return True
    return False
