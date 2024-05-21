import re

from src.line import Line
from src.part import Part
from src.section import Section
from src.song import Song

ATTRIBUTE_REGEX = "@(\\w*)=([^%]*)"
CUSTOM_ATTRIBUTE_REGEX = "!(\\w*)=([^%]*)"
SECTION_REGEX = "#\\s*([^$]*)"
CHORDS_AND_LYRICS_REGEX = "(\\[[\\w#b+/]+\\])?([^\\[]*)"


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
            else:
                SongPro.process_lyrics_and_chords(song, current_section, text)

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

    @staticmethod
    def process_lyrics_and_chords(song, current_section, text):
        if text == "":
            return

        if current_section is None:
            current_section = Section("")
            song.sections.append(current_section)

        line = Line()

        matches = re.findall(CHORDS_AND_LYRICS_REGEX, text, re.IGNORECASE)

        for match in matches:
            part = Part()

            part.chord = match[0].replace("[", "").replace("]", "")
            part.lyric = match[1]

            if part.chord != "" or part.lyric != "":
                line.parts.append(part)

        current_section.lines.append(line)
