from recipe_manager.recipe import Recipe
from sqlalchemy import select
from sqlalchemy.orm import contains_eager
from recipe_manager.database.recipe_manager_database_tables import Recipe, Ingredients
from recipe_manager.database.recipe_manager_database_session import Session


def sqlalchemy_insert(recipe_obj):
    show_recipe = recipe_obj.show_recipe
    db_recipe = create_recipe_database_object(show_recipe["recipe_title"],
                                              show_recipe["recipe_description"],
                                              show_recipe["recipe_instructions"],
                                              show_recipe["recipe_category"])
    db_ingredient = create_ingredient_database_object(recipe_obj.ingredients)
    with Session() as session:
        for ingredient in db_ingredient:
            db_recipe.ingredients.append(ingredient)
            session.add(db_recipe)
        session.commit()
        obj = session.get(Recipe, db_recipe.id)
    return obj


def sqlalchemy_select_all():
    select_all_stmt = select(Recipe).order_by(Recipe.id)
    with Session() as session:
        result = session.execute(select_all_stmt)

        for row in result.all():
            yield {f"Recipe": row.Recipe.recipe_title,
                   f"Description": row.Recipe.recipe_description,
                   f"Category": row.Recipe.recipe_category,
                   f"Instructions": row.Recipe.recipe_instructions}


def sqlalchemy_select_query_by_title(query_by_title):
    select_query_ingredients_stmt = ((select(Ingredients)
                                      .join(Ingredients.recipe)
                                      .where(Recipe.recipe_title == query_by_title)
                                      .options(contains_eager(Ingredients.recipe))
                                      .order_by(Ingredients.id)))
    select_query_recipe_stmt = select(Recipe).where(Recipe.recipe_title == query_by_title)
    with Session() as session:
        ingredient_quantity = {}
        recipe = session.execute(select_query_recipe_stmt)
        for row in session.execute(select_query_ingredients_stmt):
            ingredient_quantity[row.Ingredients.ingredient] = row.Ingredients.quantity
    return recipe.scalar(), ingredient_quantity


def validate_if_insert_query_already_exists(recipe_title):
    select_validate_recipe_stmt = select(Recipe).where(Recipe.recipe_title == recipe_title)
    with Session() as session:
        validate_result = session.execute(select_validate_recipe_stmt)
        if validate_result.scalar() is None:
            return False
        return True


def create_recipe_database_object(recipe_title, recipe_description, recipe_instructions, recipe_category):
    return Recipe(recipe_title=recipe_title,
                  recipe_description=recipe_description,
                  recipe_instructions=recipe_instructions,
                  recipe_category=recipe_category)


def create_ingredient_database_object(ingredients_list):
    for item in ingredients_list:
        ingredient = item["ingredient"]
        quantity = item["quantity"]
        yield Ingredients(ingredient=ingredient, quantity=quantity)
