import hashlib
import os
import tempfile

from gtts import gTTS

from core.audio_engine.PygletAudio import PygletAudio


class GTTSEngine(object):

    def __init__(self):
        self._temp_dir = tempfile.gettempdir()
        self._audio_engine = PygletAudio()

    def play_text(self, text):

        tts = gTTS(text=text, lang="en")
        hashed_text = hashlib.md5(text.encode("utf-8")).hexdigest()
        output_audio_file = os.path.join(self._temp_dir, hashed_text + ".mp3")
        tts.save(output_audio_file)

        self._audio_engine.play_audio_from_file(output_audio_file)





