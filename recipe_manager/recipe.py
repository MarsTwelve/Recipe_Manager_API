class Recipe:
    def __init__(self, title, description, instructions, category, ingredients_list):
        self.title = title
        self.description = description
        self.instructions = instructions
        self.category = category
        self.ingredients_list = ingredients_list
        self.ingredients = []

    def create_new_recipe(self):
        self.add_ingredients()
        recipe = {"recipe_title": self.title,
                  "recipe_description": self.description,
                  "recipe_instructions": self.instructions,
                  "recipe_category": self.category,
                  "ingredients": self.ingredients}
        return recipe

    def add_ingredients(self):
        for ingredient in self.ingredients_list:
            self.ingredients.append(Ingredients(ingredient["ingredient"], ingredient["quantity"]))


class Ingredients:
    def __init__(self, ingredient, quantity):
        self.ingredient = ingredient
        self.quantity = quantity

    def __str__(self):
        return f"{self.ingredient}, {self.quantity}"
