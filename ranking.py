"""Ranking retrieval."""
from collections import OrderedDict as dict
import itertools

from common import clean, urlopen_json
from settings import game, path, site, url
import index


def _id(mode, name):
    """The identifier for a given mode and name."""
    if mode == game.mode.star: address, key = url.id.star, site.key.star
    elif mode == game.mode.pop: address, key = url.id.pop, site.key.pop
    elif mode == game.mode.club: address, key = url.id.club, site.key.club
    elif mode == game.mode.mission: address, key = url.id.mission, site.key.mission
    else: raise ValueError("Invalid game mode")
    page = index.read()[mode][name]["page"]
    for record in urlopen_json(address.format(page), "ID retrieval"):
        if record[key["name"]] == name:
            return record[key["id"]]


def get(mode, name, chart=game.chart.nm):
    """The complete ranking of the specified mode and name.

    Arguments:
    mode -- One of the four game modes.
    name -- The full name of a disc, disc set, or mission.
    chart -- One of the four game charts.  Only relevant for Pop mode.

    """
    if mode == game.mode.star: address = url.ranking.star
    elif mode == game.mode.pop: address = url.ranking.pop
    elif mode == game.mode.club: address = url.ranking.club
    elif mode == game.mode.mission: address = url.ranking.mission
    else: raise ValueError("Invalid game mode")
    identifier = _id(mode, name)
    results = []
    for page in itertools.count(1):
        addr = address.format(identifier, page)
        if mode == game.mode.pop:
            addr += "&pt={}".format(chart["int"])
        records = urlopen_json(addr, "Ranking retrieval")
        results.extend([dict(zip(("rank", "djicon", "djname", "score"), (r["RANK"], r["DJICON"], r["DJNAME"], r["SCORE"]))) for r in records])
        if len(records) < 20:
            break
    return results
