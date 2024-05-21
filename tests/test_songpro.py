from src.songpro import SongPro


def test_parsing_custom_attributes():
    song = SongPro.parse("""
!difficulty=Easy
!spotify_url=https://open.spotify.com/track/5zADxJhJEzuOstzcUtXlXv?si=SN6U1oveQ7KNfhtD2NHf9A
""")

    assert song.custom['difficulty'] == 'Easy'
    assert song.custom[
               'spotify_url'] == "https://open.spotify.com/track/5zADxJhJEzuOstzcUtXlXv?si=SN6U1oveQ7KNfhtD2NHf9A"


def test_parsing_attributes():
    song = SongPro.parse("""
@title=Bad Moon Rising
@artist=Creedence Clearwater Revival
@capo=1st Fret
@key=C# Minor
@tempo=120
@year=1975
@album=Foo Bar Baz
@tuning=Eb Standard
""")

    assert song.title == "Bad Moon Rising"
    assert song.artist == "Creedence Clearwater Revival"
    assert song.capo == "1st Fret"
    assert song.key == "C# Minor"
    assert song.tempo == "120"
    assert song.year == "1975"
    assert song.album == "Foo Bar Baz"
    assert song.tuning == "Eb Standard"


def test_parsing_sections():
    song = SongPro.parse("""
# Verse 1
# Chorus
""")

    assert len(song.sections) == 2
    assert song.sections[0].name == "Verse 1"
    assert song.sections[1].name == "Chorus"


def test_parsing_lyrics():
    song = SongPro.parse("I don't see! a bad, moon a-rising. (a-rising)")

    assert len(song.sections) == 1
    assert len(song.sections[0].lines) == 1
    assert len(song.sections[0].lines[0].parts) == 1
    assert song.sections[0].lines[0].parts[0].lyric == "I don't see! a bad, moon a-rising. (a-rising)"


def test_parsing_parens_in_lyrics():
    song = SongPro.parse("singing something (something else)")

    assert len(song.sections) == 1
    assert len(song.sections[0].lines) == 1
    assert len(song.sections[0].lines[0].parts) == 1
    assert song.sections[0].lines[0].parts[0].lyric == "singing something (something else)"


def test_parsing_special_characters():
    song = SongPro.parse("singing sömething with Röck dots")

    assert len(song.sections) == 1
    assert len(song.sections[0].lines) == 1
    assert len(song.sections[0].lines[0].parts) == 1
    assert song.sections[0].lines[0].parts[0].lyric == "singing sömething with Röck dots"


def test_parsing_chords():
    song = SongPro.parse("[D] [D/F#] [C] [A7]")

    assert len(song.sections) == 1
    assert len(song.sections[0].lines) == 1
    assert len(song.sections[0].lines[0].parts) == 4

    assert song.sections[0].lines[0].parts[0].chord == "D"
    assert song.sections[0].lines[0].parts[0].lyric == " "
    assert song.sections[0].lines[0].parts[1].chord == "D/F#"
    assert song.sections[0].lines[0].parts[1].lyric == " "
    assert song.sections[0].lines[0].parts[2].chord == "C"
    assert song.sections[0].lines[0].parts[2].lyric == " "
    assert song.sections[0].lines[0].parts[3].chord == "A7"
    assert song.sections[0].lines[0].parts[3].lyric == ""


def test_parsing_chords_and_lyrics():
    song = SongPro.parse("[G]Don't go 'round tonight")

    assert len(song.sections) == 1
    assert len(song.sections[0].lines) == 1
    assert len(song.sections[0].lines[0].parts) == 1

    assert song.sections[0].lines[0].parts[0].chord == "G"
    assert song.sections[0].lines[0].parts[0].lyric == "Don't go 'round tonight"


def test_parsing_chords_before_lyrics():
    song = SongPro.parse("It's [D]bound to take your life")

    assert len(song.sections) == 1
    assert len(song.sections[0].lines) == 1
    assert len(song.sections[0].lines[0].parts) == 2
    assert song.sections[0].lines[0].parts[0].chord == ""
    assert song.sections[0].lines[0].parts[0].lyric == "It's "
    assert song.sections[0].lines[0].parts[1].chord == "D"
    assert song.sections[0].lines[0].parts[1].lyric == "bound to take your life"


def test_parsing_chords_after_lyrics():
    song = SongPro.parse("It's a[D]bout a [E]boy")

    assert len(song.sections) == 1
    assert len(song.sections[0].lines) == 1
    assert len(song.sections[0].lines[0].parts) == 3
    assert song.sections[0].lines[0].parts[0].chord == ""
    assert song.sections[0].lines[0].parts[0].lyric == "It's a"
    assert song.sections[0].lines[0].parts[1].chord == "D"
    assert song.sections[0].lines[0].parts[1].lyric == "bout a "
    assert song.sections[0].lines[0].parts[2].chord == "E"
    assert song.sections[0].lines[0].parts[2].lyric == "boy"


def test_augmented_chords():
    song = SongPro.parse("""
# Lyrics

[G+] This is a G Augmented chord
""")

    assert song.sections[0].lines[0].parts[0].chord == "G+"
