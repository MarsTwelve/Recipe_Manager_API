"""
SQLAlchemy validation file
"""
from database.Database import RecipeModel, Session
from sqlalchemy import select
import re


class RecipeManagerValidator:

    def __init__(self, user_input):
        self.user_input = user_input

    def space_treatment_validation(self):
        """
        Treats the user input query (recipe_title_search, update_attr, update_params), by removing leading, trailing
        and multiple spaces between chars, in the case of multiple spaces it replaces them with a single space. Both
        methods utilize the following RegEx patterns.
            Remove leading and trailing spaces --> r"^\s+|\s+$"
            Replace multiple spaces --> r"\s{2,}
        :return:
            The treated recipe title, with no spaces before and after, and with single spaces between chars
        """
        input_w_truncated_spaces = re.sub(r"^\s+|\s+$", "", self.user_input)
        treated_input = re.sub(r"\s{2,}", " ", input_w_truncated_spaces)
        self.user_input = treated_input
        return treated_input

    def has_invalid_characters(self):
        """
        Checks the given user_input for special characters, The search utilizes the following RegEx pattern to identify
        invalid characters.
            Pattern --> r"[^A-Z a-z]"
        :return: bool
            :returns True if there is a special character on the given user_input
            :returns False if there is not a special character on the given user_input
        """
        pattern_search = re.search(r"[^A-Z a-z_]", self.user_input)
        is_valid = True if pattern_search else False
        return is_valid

    def number_is_valid(self):
        """
        Made to check if the quantity number of the ingredient is in correct form
        :return: bool
        """
        number_valid = True if self.user_input > 0 else False
        return number_valid

    def has_valid_update_attr(self):
        """
        Validates if the attributes passed by the user are valid to update

        :return: bool
            :returns False if the attribute is not valid or doesn't exist
            :returns True if the attribute is valid
        """
        valid_attributes = ["recipe_title", "recipe_description", "recipe_instructions", "recipe_category", ]
        has_valid_attr = True if self.user_input in valid_attributes else False
        return has_valid_attr

    @staticmethod
    def validate_if_document_exists(treated_input, session: Session):
        """
        Validates if the requested document exists in the database

        Parameters
        ----------
        :param treated_input: str
            Receives the user input user_input, after all validation methods passed
        :param session: Session
            The database session used to execute the SQL statements
        :return: bool
            :returns: True if the document exists
            :returns: False if the document doesn't exist
        """
        select_validate_recipe_stmt = select(RecipeModel).where(RecipeModel.recipe_title == treated_input)
        validate_result = session.execute(select_validate_recipe_stmt).first()
        exists = True if validate_result else False
        return exists
