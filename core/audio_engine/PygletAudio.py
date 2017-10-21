from pyglet import app, media, clock


class PygletAudio(object):

    @staticmethod
    def _end_pyglet(_):
        app.exit()

    def play_audio_from_file(self, output_audio_file):
        song = media.load(output_audio_file)
        song.play()
        clock.schedule_once(self._end_pyglet, song.duration)
        app.run()
