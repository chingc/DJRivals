"""Index management."""
from collections import OrderedDict as dict
import json
import time

from common import urlopen_json
from settings import game, path, site, url


def create():
    """Create the index."""
    all_modes = (game.mode.star, game.mode.pop, game.mode.club, game.mode.mission)
    all_ids   = (url.id.star, url.id.pop, url.id.club, url.id.mission)
    all_pages = (site.pages.star, site.pages.pop, site.pages.club, site.pages.mission)
    all_keys  = (key["name"] for key in (site.key.star, site.key.pop, site.key.club, site.key.mission))

    index = dict()
    for mode, address, end, key in zip(all_modes, all_ids, all_pages, all_keys):
        index[mode] = dict()
        for page in range(1, end + 1):
            for record in urlopen_json(address.format(page), "Create index"):
                index[mode][record[key]] = dict(zip(("timestamp", "page"), (0, page)))
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
    index = read()
    index[mode][name]["timestamp"] = int(time.time())
    with open(path.index.db, "wb") as f:
        f.write(json.dumps(index, indent=2).encode())
