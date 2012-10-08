"""Ranking retrieval."""
import json

from common import _, _open_url
import index


def _f_id():
    """The identifier for a given mode and name."""
    def _id(mode, name):
        if mode == _.STAR:
            url  = _.STAR_ID_URL
            keys = _.DISC_KEYS
            data = star_index
        elif mode == _.POP:
            url  = _.POP_ID_URL
            keys = _.DISC_KEYS
            data = pop_index
        elif mode == _.CLUB:
            url  = _.CLUB_ID_URL
            keys = _.CLUB_KEYS
            data = club_index
        elif mode == _.MISSION:
            url  = _.MISSION_ID_URL
            keys = _.MISSION_KEYS
            data = mission_index
        else:
            raise ValueError("invalid game mode")
        for record in json.loads(_open_url(url.format(data[name]["page"])).read().decode())["DATA"]["RECORD"]:
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
        raise ValueError("invalid game mode")
    page = 1
    results = []
    identifier = _id(mode, name)
    while True:
        reply = json.loads(_open_url(url.format(identifier, page) + (("&pt=" + chart) if mode == _.POP else "")).read().decode())["DATA"]["RECORD"]
        results.extend([(record["RANK"], record["DJICON"], record["DJNAME"], record["SCORE"]) for record in reply])
        if len(reply) < 20:
            break
        page += 1
    return results


_id = _f_id()
