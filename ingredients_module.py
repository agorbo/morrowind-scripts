"""Scrape all ingredients for potions from en.uesp.net page."""
import json
import os
from telnetlib import EC

import requests
from bs4 import BeautifulSoup, Tag
from effect import Effect

import effects_module
from ingredient import Ingredient

effects = effects_module.get_effects()
effect_dict = {effect.name: effect for effect in effects}

# Get page 
URL = 'https://en.uesp.net/wiki/Morrowind:Ingredients'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')


# Get common ingredients from first table
def get_common_ingredients() -> list[Ingredient]:
    def extract_common_ingredient_name(tag: Tag) -> str:
        if (link := tag.find('a')) is not None:
            return link.text
        else:
            raise ValueError("Ingredient didn't have name.")

    def extract_common_ingredient_description(tag: Tag) -> str:
        if (td := tag.select_one('td:nth-of-type(2)')) is not None:
            return td.text
        else:
            raise ValueError("Ingredient didn't have description.")

    def extract_common_ingredient_effect_list(tag: Tag, effect_dict: dict[str, Effect]) -> list[Effect]:
        # Compose list of names of effects.
        if (effect_options := tag.select('td:nth-of-type(3) li a span')) is not None:
            effect_names = [effect_option.text for effect_option in effect_options]
        else:
            raise ValueError("Ingredient didn't have list of effects.")
        
        # Get Effect object from effect's name.
        def get_effect_by_name(effect_name: str, effect_dict: dict[str, Effect]) -> Effect:
            if (effect := effect_dict.get(effect_name)) is not None:
                return effect
            else:
                raise Exception("Effect doesn't exist in dictionary")

        return [get_effect_by_name(effect_name, effect_dict) for effect_name in effect_names]

    def extract_common_ingredient_price(tag: Tag) -> int:
        if (td := tag.select_one('.wikitable:nth-of-type(1) tr:not(:first-of-type) td:nth-of-type(4)')) is not None:
            return int(td.text)
        else:
            raise ValueError("Ingredient didn't have description.")

    def extract_common_ingredient_weight(tag: Tag) -> float:
        if (td := tag.select_one('.wikitable:nth-of-type(1) tr:not(:first-of-type) td:nth-of-type(5)')) is not None:
            return float(td.text)
        else:
            raise ValueError("Ingredient didn't have description.")

    common_ingredients_tags = soup.select('.wikitable:nth-of-type(1) tr:not(:first-of-type)')

    common_ingredients_names = [extract_common_ingredient_name(tag) for tag in common_ingredients_tags]
    common_ingredients_descriptions = [extract_common_ingredient_description(tag) for tag in common_ingredients_tags]
    common_ingredients_effect_lists = [extract_common_ingredient_effect_list(tag, effect_dict) for tag in common_ingredients_tags]
    common_ingredients_prices = [extract_common_ingredient_price(tag) for tag in common_ingredients_tags]
    common_ingredients_weights = [extract_common_ingredient_weight(tag) for tag in common_ingredients_tags]

    common_ingredients_zip = zip(common_ingredients_names, 
                                common_ingredients_descriptions,
                                common_ingredients_effect_lists, 
                                common_ingredients_prices, 
                                common_ingredients_weights)

    return [Ingredient(name, description, effect_list, price, weight) for 
        (name, description, effect_list, price, weight) in common_ingredients_zip]

def get_corpusmeat() -> list[Ingredient]:
    return []

def get_special_ingredients() -> list[Ingredient]:
    return []

# corpusmeat_tags = soup.select('.wikitable:nth-of-type(2) tr:not(:first-child) td:nth-child(2) a:first-child')
# corpusmeat_names = {link.text for link in corpusmeat_tags}
# print(len(corpusmeat_names), corpusmeat_names)
# corputsmeat = None

# special_ingredients_tags = soup.select('.wikitable:nth-of-type(3) tr:nth-child(2n) td:nth-child(2) a')
# special_ingredients_names = {link.text for link in special_ingredients_tags}
# print(len(special_ingredients_names), special_ingredients_names)
# special_ingredients = None

vanilla_ingredients = get_common_ingredients() + get_corpusmeat() + get_special_ingredients()
print(vanilla_ingredients)
