import re

from src.section import Section
from src.song import Song

ATTRIBUTE_REGEX = "@(\\w*)=([^%]*)"
CUSTOM_ATTRIBUTE_REGEX = "!(\\w*)=([^%]*)"
SECTION_REGEX = "#\\s*([^$]*)"

class SongPro:
    @staticmethod
    def parse(lines):
        song = Song()
        current_section = None

        for text in lines.split("\n"):
            if text.startswith("@"):
                SongPro.process_attribute(song, text)
            elif text.startswith("!"):
                SongPro.process_custom_attribute(song, text)
            elif text.startswith("#"):
                current_section = SongPro.process_section(song, text)
        return song

    @staticmethod
    def process_section(song, text):
        matches = re.search(SECTION_REGEX, text)
        name = matches.groups()[0]
        current_section = Section(name)
        song.sections.append(current_section)

        return current_section

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
