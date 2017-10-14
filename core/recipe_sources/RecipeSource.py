from abc import ABCMeta, abstractmethod

from typing import List

from core.recipe_sources import Recipe


class RecipeSource(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def search_recipe(self, keyword, amount):
        # type: (str, int)->List(Recipe)
        pass

    @abstractmethod
    def get_recipe_instructions(self, recipe):
        # type: (int)->List(str)
        pass
