"""Index management."""
from collections import OrderedDict as dict
import json
import time

from common import open_json
from settings import game, path, site, url


def create():
    """Create the index."""
    index = dict()
    for mode, addr, end, key in zip(game.mode.all, url.id.all, site.pages.all, (key["name"] for key in site.key.all)):
        index[mode] = dict()
        for page in range(1, end + 1):
            for record in open_json(addr.format(page), "Building index"):
                index[mode][record[key]] = dict([("timestamp", 0), ("page", page)])
    with open(path.index.db, "wb") as f:
        f.write(json.dumps(index, indent=2).encode())
    print('Wrote: "{}"'.format(path.index.db))


def read():
    """Retrieve the index."""
    with open(path.index.db, "rb") as f:
        return json.loads(f.read().decode(), object_pairs_hook=dict)


def touch(mode, name):
    """Update a timestamp.

    Arguments:
    mode -- One of the four game modes.
    name -- The full name of a disc, disc set, or mission.

    """
    data = read()
    data[mode][name]["timestamp"] = int(time.time())
    with open(path.index.db, "wb") as f:
        f.write(json.dumps(data, indent=2).encode())
