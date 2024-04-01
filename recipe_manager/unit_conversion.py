import re


class UnitConverter:

    def __init__(self, ingredients_list):
        self.ingredients_list = ingredients_list
        self.quantity = [] # The actual number
        self.unit = [] # Unit the number is measured by (raw)

    def parse_unit(self, quantity_unit):
        quantity = re.findall(r'\d+', quantity_unit)
        if len(quantity) >= 2:
            quantity = quantity[0] + "." + quantity[1]
            self.quantity = float(quantity)
        else:
            self.quantity = int(quantity[0])
        self.unit = quantity_unit[len(quantity_unit) - 2] + quantity_unit[len(quantity_unit) - 1]

    def get_unit(self):
        for ingredients in self.ingredients_list:
            quantity_unit = ingredients["quantity"]
            if "lb" in quantity_unit:
                self.parse_unit(quantity_unit)
                self.converted_units.append(self.convert_pounds_to_grams)
            if "oz" in quantity_unit:
                self.parse_unit(quantity_unit)
                self.converted_units.append(self.convert_ounces_to_grams)

    @property
    def convert_pounds_to_grams(self):
        grams = self.quantity * 453.6
        return round(grams)

    @property
    def convert_ounces_to_grams(self):
        grams = self.quantity * 28.35
        return round(grams)
