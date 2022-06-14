from enum import Enum, unique

@unique
class EffectType(str, Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"


class Effect:
    name: str
    type: EffectType

    def __init__(self, name: str, type: EffectType) -> None:
        self.name = name
        self.type = type

    def __str__(self) -> str:
        return f'{self.name} ({self.type})'
