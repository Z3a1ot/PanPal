import os
from requests import get
from typing import List

from core.recipe_sources.Recipe import Recipe
from core.recipe_sources.RecipeSource import RecipeSource

NUTRITION_API_KEY_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "resources", "nutrition_api.key")


class NutritionAPI(RecipeSource):

    base_url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/"

    def __init__(self):
        with open(NUTRITION_API_KEY_FILE, "r") as fh:
            api_key = fh.read().strip()

        self._headers = {
            "X-Mashape-Key": api_key,
            "Accept": "application/json"
        }

    def search_recipe(self, keyword, amount):
        # type: (str, int)->List(Recipe)

        raw_result = get("{}search?instructionsRequired=true&number={}&query={}&offset=0".format(self.base_url,
                                                                                                 amount, keyword),
                         headers=self._headers)

        result_json = raw_result.json()
        return [Recipe(recipe["id"], recipe["title"]) for recipe in result_json["results"]]

    def get_recipe_instructions(self, recipe_id):
        # type: (int)->List(str)

        raw_result = get("{}{}/analyzedInstructions?stepBreakdown=true".format(self.base_url, recipe_id),
                         headers=self._headers)

        result_json = raw_result.json()

        return [step["step"] for step in result_json[0]["steps"]]
