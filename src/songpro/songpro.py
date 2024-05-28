import re

SECTION_REGEX = r'#\s*([^$]*)'
ATTRIBUTE_REGEX = r'@(\w*)=([^%]*)'
CUSTOM_ATTRIBUTE_REGEX = r'!(\w*)=([^%]*)'
CHORDS_AND_LYRICS_REGEX = r'(\[[\w#b+/]+\])?([^\[]*)'

MEASURES_REGEX = r'([[\w#b/\]+\]\s]+)[|]*'
CHORDS_REGEX = r'\[([\w#b+/]+)\]?'
COMMENT_REGEX = r'>\s*([^$]*)'


class Measure:
    def __init__(self):
        self.chords = []


class Line:
    def __init__(self):
        self.parts = []
        self.comment = None
        self.tablature = None
        self.measures = None


class Part:
    def __init__(self):
        self.chord = None
        self.lyric = None


class Section:
    def __init__(self, name):
        self.name = name
        self.lines = []


class Song:
    def __init__(self):
        self.custom = {}
        self.sections = []


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

        if text.startswith("|-"):
            line.tablature = text

        elif text.startswith("| "):
            captures = re.findall(MEASURES_REGEX, text, re.I)
            measures = []

            for capture in captures:
                chords = [chord[0] for chord in re.findall(CHORDS_REGEX, capture)]
                measure = Measure()
                measure.chords = chords
                measures.append(measure)

            line.measures = measures

        elif text.startswith(">"):
            matches = re.search(COMMENT_REGEX, text)
            comment = matches.groups()[0].strip()
            line.comment = comment

        else:
            matches = re.findall(CHORDS_AND_LYRICS_REGEX, text, re.IGNORECASE)

            for match in matches:
                part = Part()

                part.chord = match[0].replace("[", "").replace("]", "")
                part.lyric = match[1]

                if part.chord != "" or part.lyric != "":
                    line.parts.append(part)

        current_section.lines.append(line)
