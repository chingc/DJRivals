"""Index management."""
from collections import OrderedDict
import json

from common import _, _exists, _open_url


def index(mode, refresh=False):
    """Create, update, or retrieve an index.

    Any of the four game mode constants defined in the common module can be
    given as the first argument.  It will create, update, or retrieve an index
    of the specified game mode.  The boolean value (default: False) controls
    whether or not to perform an index refresh by checking the DJMAX site.

    """
    if mode == _.STAR:
        url  = _.STAR_ID_URL
        key  = _.DISC_KEY["name"]
        data = _.STAR_INDEX
        last = _.STAR_PAGES
    elif mode == _.POP:
        url  = _.POP_ID_URL
        key  = _.DISC_KEY["name"]
        data = _.POP_INDEX
        last = _.POP_PAGES
    elif mode == _.CLUB:
        url  = _.CLUB_ID_URL
        key  = _.CLUB_KEY["name"]
        data = _.CLUB_INDEX
        last = _.CLUB_PAGES
    elif mode == _.MISSION:
        url  = _.MISSION_ID_URL
        key  = _.MISSION_KEY["name"]
        data = _.MISSION_INDEX
        last = _.MISSION_PAGES
    else:
        raise ValueError("invalid game mode")
    if _exists(data):
        with open(data, "rb") as f:
            index = json.loads(f.read().decode(), object_pairs_hook=dict)
    else:
        index = {}
    if refresh or not index:
        for page in range(1, last + 1):
            reply = json.loads(_open_url(url.format(page)).read().decode())["DATA"]["RECORD"]
            for record in reply:
                name = record[key]
                if name not in index:
                    index[name] = dict([("page", page), ("timestamp", 0)])
                else:
                    index[name]["page"] = page
        with open(data, "wb") as f:
            f.write(json.dumps(dict(sorted(index.items())), indent=2).encode())
        print('Wrote: "{}"'.format(data))
    return index


# reroute all dict calls to OrderedDict
dict = OrderedDict
