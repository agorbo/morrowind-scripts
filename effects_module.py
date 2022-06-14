"""Get all effects from wiki."""
import json
import os

import requests
from bs4 import BeautifulSoup, Tag

from effect import Effect, EffectType


def scrape_effects() -> None:
    # Get page and select td tags of effects 
    URL = 'https://en.uesp.net/wiki/Morrowind:Alchemy_Effects'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    tags = soup.select('.wikitable tr td:first-child')

    # Parse td tags of effects to Effect objects
    def parse_tag_to_effect(td: Tag) -> Effect:
        """Parse td tag of effect to Effect object."""
        if (effect_name_td := td.select_one('a:nth-child(2)')) is None:
            raise Exception
        effect_name = effect_name_td.text

        colors_types_dict: dict[str, EffectType] = {
            '#DDFFDD': EffectType.POSITIVE,  # green
            '#FFFFDD': EffectType.NEUTRAL,  # yellow
            '#FFDDDD': EffectType.NEGATIVE  # red
        }
        color_hex = td.attrs['style'].split("background-color:")[1][:7]
        
        if (effect_type := colors_types_dict.get(color_hex)) is None:
            raise Exception

        return Effect(effect_name, effect_type)

    effects = [parse_tag_to_effect(tag) for tag in tags]

    # Dump Effect objects to json file to store them
    with open("effects.json", "w") as outfile:
        json.dump(effects, outfile, indent=4, default=lambda obj: obj.__dict__)

def get_effects() -> list[Effect]:
    # Scrape if effects json doesn't exist
    if not os.path.exists("effects.json"):
        scrape_effects()

    # Load effects json
    with open("effects.json") as infile:
        effects_json = json.load(infile)

    # Parse json to objects
    def parse_dict_to_effect_obj(effect_dict: dict) -> Effect:
        return Effect(effect_dict['name'], EffectType(effect_dict['type']))

    effects = [parse_dict_to_effect_obj(effect_dict) for effect_dict in effects_json]

    return effects
