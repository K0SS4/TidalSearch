# TidalSearch
It's a script that lets you find tidal album ids of your already existing collection.
For it to work properly you need a directory structure like that: Library/Artist/Album Name [Year]/whatever

# Prerequisites
You need `tidalapi` package for it to work.

```bash
git clone https://github.com/k0ss4/TidalSearch
python3 -m venv TidalSearch
source TidalSearch/bin/activate
pip3 install tidalapi
```

To run it: `python3 script.py path/to/Library`  
  
After a successful run you shoud find any of these files:
- certain_ids.txt - Ids matched by artist, album and year
- uncertain_ids.txt - Ids matched by album and year
- uncertain_albums.txt - List of artists and their albums that are on the uncertain_ids.txt list
- not_found.txt - List of artists and their albums that were not found
