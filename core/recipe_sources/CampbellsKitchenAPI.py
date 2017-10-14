
from requests import get
from typing import List

from core.exceptions.RecipeSourceExpcetion import RecipeSourceException
from core.recipe_sources.Recipe import Recipe
from core.recipe_sources.RecipeSource import RecipeSource

HTTP_SUCCESS_CODE = 200


class CampbellsKitchenAPI(RecipeSource):

    def search_recipe(self, keyword, amount):
        # type: (str, int)->List(Recipe)
        pass

    def get_recipe_instructions(self, recipe):
        # type: (int)->List(str)
        pass

    url = "http://api.campbellskitchen.com/brandservice.svc/api"

    def __init__(self, app_id, app_key):
        self._app_id = app_id
        self._app_key = app_key

    def _auth_params(self):
        # type: ()->str
        return "format=json&app_id={}&app_key={}".format(self._app_id, self._app_key)

    def _get_recipe_verb(self, verb, recipe_ids):
        # type: (str, List(int))->dict
        full_url = "{}/{}/{}?{}".format(self.url, verb, "|".join(recipe_ids), self._auth_params())
        result = get(full_url)
        if result.status_code != HTTP_SUCCESS_CODE:
            raise RecipeSourceException("Invalid access {}".format(result.status_code))
        return result.json()

    def _search_by_key(self, key, value):
        full_url = "{}/search?{}&{}&{}".format(self.url, key, value, self._auth_params())
        result = get(full_url)
        if result.status_code != HTTP_SUCCESS_CODE:
            raise RecipeSourceException("Invalid access {}".format(result.status_code))
        return result.json()

    def get_recipe(self, recipe_id):
        # type: (int)->dict
        return self._get_recipe_verb("recipe", [recipe_id])

    def get_recipe_full(self, recipe_id):
        # type: (int)->dict
        return self._get_recipe_verb("recipeextended", [recipe_id])

    def get_recipe_reviews(self, recipe_id):
        # type: (int)->dict
        return self._get_recipe_verb("recipereviews", [recipe_id])

    def get_recipe_nutrition(self, recipe_id):
        # type: (int)->dict
        return self._get_recipe_verb("recipenutrition", [recipe_id])

    def get_multiple_recipes(self, recipe_ids):
        # type: (List(int))->dict
        return self._get_recipe_verb("recipe", recipe_ids)




