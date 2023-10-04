

class Container:

    nChemical = 0

    @staticmethod
    def add_chemical():
        Container.nChemical += 1

    @staticmethod
    def clear_chemical():
        Container.nChemical = 0
