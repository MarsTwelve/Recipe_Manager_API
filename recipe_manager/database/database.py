"""
Main Database Operations for the Recipe Manager
"""
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from recipe_manager.database.database_model import RecipeModel, IngredientsModel, Base
from recipe_manager.exeptions import RecipeNotFoundError


# SQLAlchemy validation, move to different file later ?
# def validate_if_insert_query_already_exists(recipe_title):
#     select_validate_recipe_stmt = select(Recipe).where(Recipe.recipe_title == recipe_title)
#     with Session() as session:
#         validate_result = session.execute(select_validate_recipe_stmt)
#         if validate_result.scalar() is None:
#             return False
#         return True


class Database:

    def __init__(self):
        # Create database engine
        self.engine = create_engine("mysql+pymysql://root:password@localhost/recipe_manager")
        Base.metadata.create_all(self.engine)

    def sqlalchemy_insert_recipe(self, recipe_obj, session: Session):
        """
        Inserts Recipe into the database

        Parameters
        ----------
        :param recipe_obj: python object
            Should receive a python object containing all the recipe information
        :param session: Session
            Database session object for database operations
        :return: SQL Model of Recipe (RecipeModel) and inserted recipe id
            Returns a SQL Model of the RecipeModel class, also returns the inserted recipe id
        """
        show_recipe = recipe_obj.show_recipe
        db_recipe = RecipeModel(recipe_title=show_recipe["recipe_title"],
                                recipe_description=show_recipe["recipe_description"],
                                recipe_instructions=show_recipe["recipe_instructions"],
                                recipe_category=show_recipe["recipe_category"])

        for ingredients in recipe_obj.ingredients:
            ingredient = ingredients["ingredient"]
            quantity = ingredients["quantity"]
            db_recipe.ingredients.append(IngredientsModel(ingredient=ingredient, quantity=quantity))
        session.add(db_recipe)
        session.commit()
        return session.get(RecipeModel, db_recipe.id)

    def sqlalchemy_select_query_by_title(self, query_param, session: Session):
        select_query_ingredients_stmt = ((select(RecipeModel)
                                          .join(RecipeModel.ingredients)
                                          .where(RecipeModel.recipe_title == query_param)
                                          .order_by(RecipeModel.id)))
        result_raw = session.execute(select_query_ingredients_stmt)
        result = result_raw.scalar()
        if result:
            recipe = {"recipe_title": result.recipe_title,
                      "recipe_description": result.recipe_description,
                      "recipe_instructions": result.recipe_instructions,
                      "recipe_category": result.recipe_category}
            ingredient_quantity = {}
            for row in result.ingredients:
                ingredient_quantity[row.ingredient] = row.quantity
            return recipe, ingredient_quantity
        raise RecipeNotFoundError

    def sqlalchemy_select_all(self, session: Session):
        select_all_stmt = select(RecipeModel).order_by(RecipeModel.id)
        result = session.execute(select_all_stmt)
        for row in result.all():
            yield {
                "Recipe": row.RecipeModel.recipe_title,
                "Description": row.RecipeModel.recipe_description,
                "Category": row.RecipeModel.recipe_category,
                "Instructions": row.RecipeModel.recipe_instructions
            }

    def sqlalchemy_update_recipe_title(self, recipe_title, update_attr, update_param, session: Session):
        """
        Updates a specific recipe on the database
        """
        recipe_to_update = session.execute(select(RecipeModel).where(RecipeModel.recipe_title == recipe_title)).scalar()
        recipe_id = recipe_to_update.id
        recipe_to_update.recipe_title = update_param
        setattr(recipe_to_update, update_attr, update_param)
        recipe_updated = session.execute(select(RecipeModel).where(RecipeModel.id == recipe_id)).scalar()
        return recipe_updated


    def sqlalchemy_delete_all(self, session: Session):
        """
        Deletes all recipes from the database

        Parameters
        ----------
        :param session:
            The database session
        :return:
            None
        """
        stmt = select(RecipeModel)
        results = session.execute(stmt)
        for result in results.scalars():
            session.delete(result)
            session.commit()

        # Confirm deletion
        results_post_deletion = session.execute(stmt)
        recipes_post_deletion = results_post_deletion.all()

        if not recipes_post_deletion:
            print("All recipes deleted")
        else:
            raise Exception("[ERR] - Recipes were not deleted")

    def sqlalchemy_delete_recipe(self, query_param, session: Session):
        """
        Deletes a recipe from the database

        Parameters
        ----------
        :param:query_param: str
            The parameter used to make the query statement, for now, recipe title is used
        :param:session (Session)
            The database session used to execute the SQL statements
        """
        stmt = select(RecipeModel).where(RecipeModel.recipe_title == query_param)
        result = session.execute(stmt)
        recipe = result.scalar()

        if recipe:
            # Delete the recipe
            session.delete(recipe)
            session.commit()

            # Confirm deletion
            result_post_deletion = session.execute(stmt)
            recipe_post_deletion = result_post_deletion.first()
            if recipe_post_deletion is None:
                print("Recipe was successfully deleted")
            else:
                raise Exception("[ERR] - Recipes were not deleted")
        else:
            raise RecipeNotFoundError
