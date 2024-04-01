class Recipe:
    def __init__(self, title, description, instructions, category):
        self.title = title
        self.description = description
        self.instructions = instructions
        self.category = category
        self.ingredients = []

    @property
    def show_recipe(self):
        recipe = {"recipe_title": self.title,
                  "recipe_description": self.description,
                  "recipe_instructions": self.instructions,
                  "recipe_category": self.category}
        return recipe

    def add_ingredients(self, ingredients):
        for ingredient in ingredients:
            self.ingredients.append(Ingredients(ingredient["ingredient"], ingredient["quantity"]))


class Ingredients:
    def __init__(self, ingredient, quantity):
        self.ingredient = ingredient
        self.quantity = quantity

    def __getitem__(self, item):
        if item == "ingredient":
            return self.ingredient
        if item == "quantity":
            return self.quantity
