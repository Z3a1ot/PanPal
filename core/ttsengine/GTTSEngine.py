import hashlib
import tempfile

import os

from gtts import gTTS


class GTTSEngine(object):

    def __init__(self):
        self._temp_dir = tempfile.gettempdir()

    def play_text(self, text):

        tts = gTTS(text=text, lang="en")
        hashed_text = hashlib.md5(text).hexdigest()
        output_audio_file = os.path.join(self._temp_dir, hashed_text, ".mp3")
        tts.save(output_audio_file)

        os.system("open {}".format(output_audio_file))

