from unittest import TestCase

from src.songpro import SongPro


class TestSongPro(TestCase):

    def test_parsing_custom_attributes(self):
        song = SongPro.parse("""
!difficulty=Easy
!spotify_url=https://open.spotify.com/track/5zADxJhJEzuOstzcUtXlXv?si=SN6U1oveQ7KNfhtD2NHf9A
""")

        self.assertEqual(song.custom['difficulty'], 'Easy')
        self.assertEqual(song.custom['spotify_url'],
                         "https://open.spotify.com/track/5zADxJhJEzuOstzcUtXlXv?si=SN6U1oveQ7KNfhtD2NHf9A")

    def test_parsing_attributes(self):
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

        self.assertEqual(song.title, "Bad Moon Rising")
        self.assertEqual(song.artist, "Creedence Clearwater Revival")
        self.assertEqual(song.capo, "1st Fret")
        self.assertEqual(song.key, "C# Minor")
        self.assertEqual(song.tempo, "120")
        self.assertEqual(song.year, "1975")
        self.assertEqual(song.album, "Foo Bar Baz")
        self.assertEqual(song.tuning, "Eb Standard")
