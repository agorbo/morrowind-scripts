from effect import Effect


class Ingredient:
    name: str
    description: str
    effectList: list[Effect]
    price: int
    weight: float

    def __init__(self, name, description, effectList, price, weight) -> None:
        self.name = name
        self.description = description
        self.effectList = effectList
        self.price = price
        self.weight = weight
    