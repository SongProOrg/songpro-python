# SongPro for Python

[SongPro](https://songpro.org) is a text format for transcribing songs.
 
This project is a Python library that converts the song into a Song data model which can then be converted into various output formats such as text or HTML.

## Installation

Install using `pip`:

```shell
$ python -m pip install songpro
```

## Usage

Given the file `escape-capsule.sng` with the following contents:

```
@title=Escape Capsule
@artist=Brian Kelly
!bandcamp=https://spilth.bandcamp.com/track/escape-capsule-nashville-edition

# Verse 1

Climb a-[D]board [A]
I've been [Bm]waiting for you [F#m]
Climb a-[G]board [D]
You'll be [Asus4]safe in [A7]here

# Chorus 1

[G] I'm a [D]rocket [F#]made for your pro-[Bm]tection
You're [G]safe with me, un-[A]til you leave
```

You can then parse the file to create a `Song` object:

```python
from songpro import SongPro

with open('escape-capsule.sng', 'r') as file:
  text = file.read()

song = SongPro.parse(text)

print(song.title)
# Escape Capsule

print(song.arist)
# Brian Kelly

print(song.sections[1].name)
# Chorus 1
```

## Development

After checking out the project, set up venv, install dependencies and run the default task that tests and builds the project:

```bash
$ git clone git@github.com:SongProOrg/songpro-python.git
$ cd songpro-python
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install invoke build pytest twine
$ invoke --list
$ invoke
```

## Contributing

Bug reports and pull requests are welcome on GitHub at <https://github.com/SongProOrg/songpro-python>.

## License

The library is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
