from unittest import TestCase

from core.ttsengine.GTTSEngine import GTTSEngine


class TestGTTSEngine(TestCase):

    def test_play_text(self):
        tts = GTTSEngine()
        tts.play_text("Hello!")

