"""Ranking retrieval."""
from urllib.request import urlopen
import json

from common import _
import index


def _f_id():
    """The identifier for a given mode and name."""
    def _id(mode, name):
        if mode == _.STAR:
            url   = _.STAR_ID_URL
            keys  = _.DISC_KEYS
            idata = star_index
        elif mode == _.POP:
            url   = _.POP_ID_URL
            keys  = _.DISC_KEYS
            idata = pop_index
        elif mode == _.CLUB:
            url   = _.CLUB_ID_URL
            keys  = _.CLUB_KEYS
            idata = club_index
        elif mode == _.MISSION:
            url   = _.MISSION_ID_URL
            keys  = _.MISSION_KEYS
            idata = mission_index
        else:
            raise ValueError("invalid argument")
        data = json.loads(urlopen(url.format(idata[name]["page"])).read().decode())["DATA"]["RECORD"]
        for record in data:
            if record[keys["name"]] == name:
                return record[keys["id"]]

    star_index    = index.touch(_.STAR)
    pop_index     = index.touch(_.POP)
    club_index    = index.touch(_.CLUB)
    mission_index = index.touch(_.MISSION)
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
