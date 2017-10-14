from unittest import TestCase

from core.recipe_sources.NutritionAPI import NutritionAPI


class TestNutritionAPI(TestCase):

    def test_search_recipe(self):

        napi = NutritionAPI()

        result = napi.search_recipe("burger", 1)

        self.assertEqual(len(result), 1)
        self.assertIs(type(result[0].id), int)
        self.assertIs(type(result[0].name), unicode)
        print("{}".format(result))

    def test_instructions(self):

        napi = NutritionAPI()

        recipe_id = 690978
        result = napi.get_recipe_instructions(recipe_id)

        self.assertGreater(len(result), 0)
        for k, v in enumerate(result):
            self.assertIs(type(v), unicode)

        print("{}".format(result))

