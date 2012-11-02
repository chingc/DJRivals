"""Ranking retrieval."""
import json
import re

from common import _, _open_url
from index import index


def _id(mode, name):
    """The identifier for a given mode and name."""
    if mode == _.STAR:
        url  = _.STAR_ID_URL
        key  = _.DISC_KEY
        data = index(_.STAR)
    elif mode == _.POP:
        url  = _.POP_ID_URL
        key  = _.DISC_KEY
        data = index(_.POP)
    elif mode == _.CLUB:
        url  = _.CLUB_ID_URL
        key  = _.CLUB_KEY
        data = index(_.CLUB)
    elif mode == _.MISSION:
        url  = _.MISSION_ID_URL
        key  = _.MISSION_KEY
        data = index(_.MISSION)
    else:
        raise ValueError("invalid game mode")
    for record in json.loads(_open_url(url.format(data[name]["page"]), "retrieving ID").read().decode())["DATA"]["RECORD"]:
        if record[key["name"]] == name:
            return record[key["id"]]


def ranking(mode, name, chart="nm"):
    """The complete ranking of the specified mode and name.

    Any of the four game mode constants defined in the common module can be
    given as the first argument.  The name must be the complete name of a disc,
    disc set, or mission.  The chart is a key from the CHART dictionary defined
    in the common module.  It is only relevant to Pop Mode, and defaults to the
    value of the "nm" key.

    """
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
        reply = json.loads(_open_url(url.format(identifier, page) + (("&pt=" + _.CHART[chart]) if mode == _.POP else ""), "retrieving '{}'".format(re.sub(r"[^a-zA-Z0-9_- ]", r"", name))).read().decode())["DATA"]["RECORD"]
        results.extend((record["RANK"], record["DJICON"], record["DJNAME"], record["SCORE"]) for record in reply)
        if len(reply) < 20:
            break
        page += 1
    return results
