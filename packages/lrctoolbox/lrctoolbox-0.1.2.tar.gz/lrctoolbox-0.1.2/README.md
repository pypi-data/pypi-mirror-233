# Toolkit to work with [LRC Files](https://en.wikipedia.org/wiki/LRC_(file_format)) in Python

[![PyPI version](https://badge.fury.io/py/lrctoolbox.svg)](https://badge.fury.io/py/lrctoolbox) ![Test](https://github.com/Dr-Blank/lrctoolbox/actions/workflows/tests.yaml/badge.svg)
## Usage

```python
from lrctoolbox import SyncedLyrics

# Load LRC file
lyrics = SyncedLyrics.load_from_file("example.lrc")

# check if lyrics are synced
assert lyrics.is_synced

# get lyrics as string
print(lyrics.lyrics)

# shift lyrics by 1 second
for line in lyrics.lines:
    line.timestamp += 1000

```

## Development

poetry is used for dependency management. Install it with `pip install poetry` and then run `poetry install` to install all dependencies.


