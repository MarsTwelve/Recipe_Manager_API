class Recipe:
    """
    A class to represent a Recipe Object.
    ...

    Attributes
    ----------
    title: str
        contains the recipe title
    description: str
        short description of the given recipe
    instructions: str
        contains instructions on how the recipe should be made
    category: str
        represents the food category of the recipe
    ingredients: list
        contains a list composed of small python dicts, storing the ingredients of the given recipe
        Eg: {"ingredient": flour,
            "quantity": 5_oz}

    Methods
    ---------
    @property
    show_recipe()
        Returns a dict object that contains all parameters of the current instantiated recipe

    add_ingredients(ingredients)
        Receives a list of python dictionaries, containing the ingredients and quantities of a given recipe,
        then it constructs multiple Ingredient objects and stores it within its own instance.
    """

    def __init__(self, title, description, instructions, category):
        """
        Initializes all the necessary class variables to make a Recipe object.

        Parameters
        -----------
        :param title: str
            contains the title of the recipe
        :param description: str
            contains a brief description of the recipe
        :param instructions: str
            contains a set of instructions on how the recipe should be made
        :param category: str
            contains the food group category the recipe falls into
        """
        self.title = title
        self.description = description
        self.instructions = instructions
        self.category = category
        self.ingredients = []

    @property
    def show_recipe(self):
        """
        Returns a python dict of the given recipe
        :return:
            returns a python dict of the given recipe object
            Eg: {"recipe_title": self. title,
                "recipe_description": self. description,
                "recipe_instructions": self. instructions,
                "recipe_category": self. category}
        """
        recipe = {"recipe_title": self.title,
                  "recipe_description": self.description,
                  "recipe_instructions": self.instructions,
                  "recipe_category": self.category}
        return recipe

    def add_ingredients(self, ingredients):
        """
        Adds the given ingredients list as Ingredient objects into the Recipe object
        :param ingredients: list
            A list containing the ingredients needed for the recipe, should be a list of dictionaries
        :return:
        None
        """
        for ingredient in ingredients:
            print(ingredients)
            self.ingredients.append(Ingredients(ingredient["ingredient"], ingredient["quantity"], ingredient["unit"]))


class Ingredients:
    """
    Represents a specific ingredient and its quantity
    ...
    Attributes
    ----------
    ingredient: str
        contains the ingredient name
    quantity: str
        contains the quantity of the given ingredient
    unit: str
        Contains the unit used to measure said ingredient (ounces/oz, pounds/lb or grams/gr)
    """

    def __init__(self, ingredient, quantity, unit):
        """
        Initializes all the necessary class variables to make a Recipe object.

        Parameters
        ----------
        :param ingredient: str
            The actual name of the ingredient
        :param quantity: str
            The quantity of said ingredient,
        :param unit: str
            The unit witch the ingredient is measured by
        """
        self.ingredient = ingredient
        self.quantity = quantity
        self.unit = unit

    def __getitem__(self, item):
        if item == "ingredient":
            return self.ingredient
        if item == "quantity":
            return self.quantity
        if item == "unit":
            return self.unit
