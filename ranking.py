"""Ranking retrieval."""
import json

from common import _, _open_url
import index


def _f_id():
    """The identifier for a given mode and name."""
    def _id(mode, name):
        if mode == _.STAR:
            url  = _.STAR_ID_URL
            key  = _.DISC_KEY
            data = star_index
        elif mode == _.POP:
            url  = _.POP_ID_URL
            key  = _.DISC_KEY
            data = pop_index
        elif mode == _.CLUB:
            url  = _.CLUB_ID_URL
            key  = _.CLUB_KEY
            data = club_index
        elif mode == _.MISSION:
            url  = _.MISSION_ID_URL
            key  = _.MISSION_KEY
            data = mission_index
        else:
            raise ValueError("invalid game mode")
        for record in json.loads(_open_url(url.format(data[name]["page"])).read().decode())["DATA"]["RECORD"]:
            if record[key["name"]] == name:
                return record[key["id"]]

    star_index    = index.index(_.STAR)
    pop_index     = index.index(_.POP)
    club_index    = index.index(_.CLUB)
    mission_index = index.index(_.MISSION)
    return _id


def ranking(mode, name, chart=None):
    """The complete ranking of the specified mode and name."""
    if mode == _.STAR:
        url = _.STAR_RANKING_URL
    elif mode == _.POP:
        url = _.POP_RANKING_URL
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
