"""Ranking retrieval."""
from urllib.request import urlopen
import json

from common import _
import index


def _f_id():
    """The identifier for a given mode and name."""
    def _id(mode, name):
        # DJMAX returns up to 20 identifiers at a time (each page contains 20
        # except the last page which may contain less), so this function uses a
        # cache to expedite future lookups.  However, since it is unknown how
        # long these identifiers stay valid, the cache is set to automatically
        # clear itself and rebuild once it exceeds a certain capacity.
        if mode == _.STAR:
            url   = _.STAR_ID_URL
            idata = star_index
            cache = star_cache
            nkey  = "DISCNAME"
            idkey = "DISCID"
        elif mode == _.POP:
            url   = _.POP_ID_URL
            idata = pop_index
            cache = pop_cache
            nkey  = "DISCNAME"
            idkey = "DISCID"
        elif mode == _.CLUB:
            url   = _.CLUB_ID_URL
            idata = club_index
            cache = club_cache
            nkey  = "DISCSETNAME"
            idkey = "DISCSETID"
        elif mode == _.MISSION:
            url   = _.MISSION_ID_URL
            idata = mission_index
            cache = mission_cache
            nkey  = "MISSIONPACKNAME"
            idkey = "MISSIONPACKID"
        else:
            raise ValueError("invalid argument")
        if name not in cache:
            if len(cache) > 40:  # value of 40 means at most 60 entries
                cache.clear()
            data = json.loads(urlopen(url.format(idata[name]["page"])).read().decode())["DATA"]["RECORD"]
            cache.update({record[nkey]: record[idkey] for record in data})
        return cache[name]

    star_index    = index.touch(_.STAR)
    pop_index     = index.touch(_.POP)
    club_index    = index.touch(_.CLUB)
    mission_index = index.touch(_.MISSION)
    star_cache    = {}
    pop_cache     = {}
    club_cache    = {}
    mission_cache = {}
    return _id


def _ranking(mode, name, chart=None):
    """The complete ranking of the specified mode and name."""
    if mode == _.STAR:
        url = _.STAR_RANKING_URL
    elif mode == _.POP:
        url = _.POP_RANKING_URL
        chart = (lambda x: "1" if x == "nm" else "2" if x == "hd" else "3" if x == "mx" else "4")(chart)
    elif mode == _.CLUB:
        url = _.CLUB_RANKING_URL
    elif mode == _.MISSION:
        url = _.MISSION_RANKING_URL
    else:
        raise ValueError("invalid argument")
    identifier = _id(mode, name)
    results = []
    for page in range(1, 100):
        data = json.loads(urlopen(url.format(identifier, page) + (("&pt=" + chart) if mode == _.POP else "")).read().decode())["DATA"]["RECORD"]
        results.extend([(record["RANK"], record["DJICON"], record["DJNAME"], record["SCORE"]) for record in data])
        if len(data) < 20:
            break
    return results


_id = _f_id()
