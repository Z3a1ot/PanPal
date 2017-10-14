import hashlib
import tempfile

import os

import sys
from gtts import gTTS

import gi

gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

import pygst
pygst.require('0.10')
import gst
import gobject
import os

def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        sys.stdout.write("End-of-stream\n")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write("Error: %s: %s\n" % (err, debug))
        loop.quit()
    return True

class GTTSEngine(object):

    def __init__(self):
        self._temp_dir = tempfile.gettempdir()

    def play_text(self, text):

        tts = gTTS(text=text, lang="en")
        hashed_text = hashlib.md5(text).hexdigest()
        tts.save(os.path.join(self._temp_dir, hashed_text, ".mp3"))



        mainloop = gobject.MainLoop()
        pl = gst.element_factory_make("playbin", "player")
        pl.set_property('uri', 'file://' + os.path.abspath('thesong.ogg'))
        pl.set_state(gst.STATE_PLAYING)
        mainloop.run()

        GObject.threads_init()
        Gst.init(None)

        playbin = Gst.ElementFactory.make("playbin", None)
        if not playbin:
            sys.stderr.write("'playbin' gstreamer plugin missing\n")
            sys.exit(1)

        # take the commandline argument and ensure that it is a uri
        if Gst.uri_is_valid(args[1]):
            uri = args[1]
        else:
            uri = Gst.filename_to_uri(args[1])
        playbin.set_property('uri', uri)

        # create and event loop and feed gstreamer bus mesages to it
        loop = GObject.MainLoop()

        bus = playbin.get_bus()
        bus.add_signal_watch()
        bus.connect("message", bus_call, loop)

        # start play back and listed to events
        playbin.set_state(Gst.State.PLAYING)
        try:
            loop.run()
        except:
            pass

        # cleanup
        playbin.set_state(Gst.State.NULL)