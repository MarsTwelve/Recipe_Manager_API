from endpoints.RecipeManagerValidator import RecipeManagerValidator


def validate_recipe_input(recipe_dict):
    """
    Validates the user submitted recipe information, validating against empty fields, invalid chars such as special
    characters and digits (underscores are allowed)
    :param recipe_dict: dict
        a dicy that contains the information about the recipe
    :return:
        :returns: treated_recipe: dict
            In the case the validation passes, a new dict called treated_recipe is returned, ready for insertion on the
            database
        :returns: str
            In the case the validation fails, it should return a string that contains the error found during validation
    """
    treated_recipe = {}

    for value in recipe_dict:

        if value == "ingredients":
            validated_list_response = validate_ingredients_list(recipe_dict[value])
            if not isinstance(validated_list_response, list):
                return validated_list_response
            treated_recipe["ingredients"] = validated_list_response
            return treated_recipe

        valid_input = RecipeManagerValidator(recipe_dict[value])
        treated_input = valid_input.space_treatment_validation()

        if not treated_input:
            return f"[ERR]EMPTY_FIELD - Empty fields are not allowed here --> {value}. Please provide a value."

        if valid_input.has_invalid_characters():
            return (f"[ERR]VALIDATION_FAILED - Special characters and digits are not allowed here"
                    f" --> {recipe_dict[value]}")

        # Ask caio if these sets of if statements are redundant
        if value == "title":
            treated_recipe["recipe_title"] = treated_input
            continue

        if value == "description":
            treated_recipe["recipe_description"] = treated_input
            continue

        if value == "instructions":
            treated_recipe["recipe_instructions"] = treated_input
            continue

        if value == "category":
            treated_recipe["recipe_category"] = treated_input
            continue


def validate_ingredients_list(ingredients_list):
    """
    Validates the list of ingredients contained within the recipe dict
    :param ingredients_list: list
        a list of dicts containing information about the ingredients utilized on the recipe
        eg: [
                {
                    ingredient: flour,
                    quantity: 2,
                    unit: lb,
                },
                {
                    ingredient: generic powder,
                    quantity: 0.5,
                    unit: lb,
                },
            ]
    :return: treated_ingredients_list: list
        :returns in the case the validation succeeds a list of dicts, witch passed through validation successfully
        :returns a string in the case validation failed, explaining the specific error that caused the validation to
        fail, such as empty fields, or invalid chars eg: Fl0ur or Whe@t
    """
    treated_ingredients_list = []

    for ingredient_dict in ingredients_list:
        treated_ingredients = {}
        for ingredient_attr in ingredient_dict:
            valid_input = RecipeManagerValidator(ingredient_dict[ingredient_attr])

            if ingredient_attr == "quantity":
                if not valid_input.number_is_valid():
                    return ("[ERR]INVALID_NUMBER - The number provided is either 0 or negative. "
                            "Please provide a positive number")
                treated_ingredients["quantity"] = ingredient_dict[ingredient_attr]
                continue

            treated_input = valid_input.space_treatment_validation()
            if not treated_input:
                return "[ERR]EMPTY_FIELD - Empty fields are not allowed. Please provide a value."

            if valid_input.has_invalid_characters():
                return (f"[ERR]VALIDATION_FAILED - Special characters and digits are not allowed here"
                        f" --> {ingredient_dict[ingredient_attr]}")

            if ingredient_attr == "ingredient":
                treated_ingredients["ingredient"] = treated_input
                continue

            if ingredient_attr == "unit":
                if treated_input not in ("lb", "oz", "gr"):
                    return ("[ERR]INVALID_UNIT - The unit provided is invalid. The only acceptable unit types are: "
                            "pounds(lb), ounces (oz) and grams (gr). ")
                treated_ingredients["unit"] = treated_input
                treated_ingredients_list.append(treated_ingredients)
    return treated_ingredients_list
