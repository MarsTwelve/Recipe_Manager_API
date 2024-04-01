import re


class UnitConverter:

    def __init__(self, ingredients_list):
        self.ingredients_list = ingredients_list
        self.quantity = [] # The actual number
        self.unit = [] # Unit the number is measured by (raw)

    def parse_ingredients_list(self, quantity_unit):
        quantity = re.findall(r'\d+', quantity_unit)
        if len(quantity) >= 2:
            quantity = quantity[0] + "." + quantity[1]
            self.quantity.append(float(quantity))
        else:
            self.quantity.append(int(quantity[0]))
        self.unit.append(quantity_unit[len(quantity_unit) - 2] + quantity_unit[len(quantity_unit) - 1])

    def get_unit(self):
        for ingredients in self.ingredients_list:
            quantity_unit = ingredients.quantity
            if "lb" in quantity_unit:
                self.parse_ingredients_list(quantity_unit)
                # Change later for a convert method
            if "oz" in quantity_unit:
                self.parse_ingredients_list(quantity_unit)
                # Change later for a convert method

    @property
    def convert_pounds_to_grams(self):
        converted = []
        for quantity in self.quantity:
            converted.append(round(quantity * 453.6))
        return converted

    @property
    def convert_ounces_to_grams(self):
        converted = []
        for quantity in self.quantity:
            converted.append(round(quantity * 28.35))
        return converted
