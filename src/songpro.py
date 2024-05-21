import re

from src.song import Song

ATTRIBUTE_REGEX = "@(\\w*)=([^%]*)"
CUSTOM_ATTRIBUTE_REGEX = "!(\\w*)=([^%]*)"


class SongPro:
    @staticmethod
    def parse(lines):
        song = Song()

        for text in lines.split("\n"):
            if text.startswith("@"):
                SongPro.process_attribute(song, text)
            elif text.startswith("!"):
                SongPro.process_custom_attribute(song, text)
        return song

    @staticmethod
    def process_attribute(song, text):
        matches = re.search(ATTRIBUTE_REGEX, text)
        key = matches.groups()[0]
        value = matches.groups()[1]

        attributes = {"title", "artist", "capo", "key", "tempo", "year", "album", "tuning"}
        if key in attributes:
            setattr(song, key, value)
        else:
            print("WARNING: Unknown attribute " + key)

    @staticmethod
    def process_custom_attribute(song, text):
        matches = re.search(CUSTOM_ATTRIBUTE_REGEX, text)
        key = matches.groups()[0]
        value = matches.groups()[1]

        song.custom[key] = value
