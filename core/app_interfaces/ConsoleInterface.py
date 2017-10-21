import shlex
import sys

import os
import traceback

from typing import List

from core.exceptions.InvalidFlowException import InvalidFLowExpcetion
from core.exceptions.InvalidRecipeIdException import InvalidRecipeIdException
from core.recipe_sources.NutritionAPI import NutritionAPI
from core.recipe_sources.Recipe import Recipe
from core.ttsengine.GTTSEngine import GTTSEngine

NEXT_COMMAND = "next"
START_COMMAND = "start"
SEARCH_COMMAND = "search"
EXIT_COMMAND = "exit"
REPEAT_COMMAND = "repeat"


class ConsoleInterface(object):
    def __init__(self):
        self._commands = {
            "help, ?": "Prints this message",
            EXIT_COMMAND: "Exits this application",
            SEARCH_COMMAND: "Searches for a recipe given a keyword",
            START_COMMAND: "Start guiding recipe of id from 'search'",
            NEXT_COMMAND: "Next instruction from started recipe"
        }
        self._recipe_source = NutritionAPI()
        self._tts_engine = GTTSEngine()
        self._recipe_list = None  # type: List(Recipe)
        self._instruction_list = None
        self._instruction_index = 0

    def search_recipes(self, key):
        # type: (str)->None
        recipe_query_amount = 10
        self._recipe_list = self._recipe_source.search_recipe(key, recipe_query_amount)

        for index, recipe in enumerate(self._recipe_list):
            sys.stdout.write("{}: {}{}".format(index, recipe.name, os.linesep))

    def start_recipe(self, recipe_id):
        # type: (int)->None
        if not self._recipe_list:
            raise InvalidFLowExpcetion("Invalid flow, you need to search for recipes first")
        if recipe_id >= len(self._recipe_list):
            raise InvalidRecipeIdException("Invalid recipe id {}".format(recipe_id))

        self._instruction_list = self._recipe_source.get_recipe_instructions(self._recipe_list[recipe_id].id)
        self._instruction_index = 0
        self._tts_engine.play_text("Starting recipe: {}".format(self._recipe_list[recipe_id].name))

    def play_current_instruction(self):
        if self._instruction_index == len(self._instruction_list):
            raise InvalidFLowExpcetion("Recipe is done")
        current_instruction = self._instruction_list[self._instruction_index]
        sys.stdout.write("{}{}".format(current_instruction, os.linesep))
        self._tts_engine.play_text(current_instruction)

    def next_instruction(self):
        self._instruction_index += 1
        if self._instruction_index == len(self._instruction_list):
            self._tts_engine.play_text("All done!")

    def main(self):
        sys.stdout.write("PanPal version 0.1.{}".format(os.linesep))
        sys.stdout.write("Search for a recipe and I will guide you through it.{}".format(os.linesep))

        while True:
            prompt = "> "
            try:
                input_list = shlex.split(raw_input(prompt))
                if len(input_list) == 0:
                    continue
                cmd = input_list[0]
                print(cmd)
                if cmd == EXIT_COMMAND:
                    break
                elif cmd == "help" or cmd == "?":
                    self._print_help()
                elif cmd == SEARCH_COMMAND:
                    self.search_recipes(input_list[1])
                elif cmd == START_COMMAND:
                    self.start_recipe(int(input_list[1]))
                elif cmd == REPEAT_COMMAND:
                    self.play_current_instruction()
                elif cmd == NEXT_COMMAND:
                    self.play_current_instruction()
                    self.next_instruction()
                else:
                    sys.stderr.write("Unknown command: {}{}".format(input_list, os.linesep))
            except Exception as e:
                sys.stderr.write("{}{}".format(e, os.linesep))
                sys.stderr.write(traceback.format_exc())
        sys.stdout.write("Bye!{}".format(os.linesep))
        return 0

    def _print_help(self):
        for command in self._commands:
            sys.stdout.write("{} - {}{}".format(command, self._commands[command], os.linesep))
