import re


class Song:
    def __init__(self):
        self.title = "None"


class SongPro:
    @staticmethod
    def parse(lines):
        song = Song()

        for text in lines.split("\n"):
            if text.startswith("@"):
                SongPro.process_attribute(song, text)

        return song

    @staticmethod
    def process_attribute(song, text):
        matches = re.search("@(\\w*)=([^%]*)", text)
        key = matches.groups()[0]
        value = matches.groups()[1]

        attributes = {"title", "artist", "capo", "key", "tempo", "year", "album", "tuning"}
        if key in attributes:
            setattr(song, key, value)
        else:
            print("WARNING: Unknown attribute " + key)



