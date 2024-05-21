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
