"""Database record generator."""
from collections import OrderedDict as dict
import json
import zlib

from common import clean, ls, mkdir
from settings import game, path
import ranking


def create(mode, name):
    """Create a local record of the specified mode and name.

    Arguments:
    mode -- One of the four game modes.
    name -- The full name of a disc, disc set, or mission.

    """
    all_charts    = (game.chart.nm, game.chart.hd, game.chart.mx, game.chart.ex)
    all_pop_paths = (path.db.nm, path.db.hd, path.db.mx, path.db.ex)

    if mode == game.mode.star: level = [(game.chart.nm, path.db.star)]
    elif mode == game.mode.pop: level = zip(all_charts, all_pop_paths)
    elif mode == game.mode.club: level = [(game.chart.nm, path.db.club)]
    elif mode == game.mode.mission: level = [(game.chart.nm, path.db.mission)]
    else: raise ValueError("Invalid game mode")
    for chart, directory in level:
        results = ranking.get(mode, name, chart)
        if results:
            clean_name = clean(name)
            record = dict()
            record["name"] = name
            record["eyecatch"] = "{}.png".format(clean_name)
            record["icon"] = "{}_{}.png".format(clean_name, chart["int"])
            record["ranking"] = results
            with open(directory + clean_name + ".json", "wb") as f:
                f.write(json.dumps(record, indent=1).encode())
            print('Wrote: "{}{}.json"'.format(directory, clean_name))


def dj():
    """Use the local database to create a record for each DJ."""
    def extract(directory):
        names = dict()
        for record in ls(directory):
            with open(directory + record, "rb") as f:
                disc = json.loads(f.read().decode())
            all_dj.update((dj["djname"], dj["djicon"]) for dj in disc["ranking"])
            names[disc["name"]] = (9999, 0)  # default rank and score
        return names

    def fill(mode, directory):
        for record in ls(directory):
            with open(directory + record, "rb") as f:
                disc = json.loads(f.read().decode())
            for dj in disc["ranking"]:
                all_dj[dj["djname"]][mode][disc["name"]] = (dj["rank"], dj["score"])

    all_type    = (game.mode.star, game.chart.nm["str"], game.chart.hd["str"], game.chart.mx["str"], game.chart.ex["str"], game.mode.club, game.mode.mission)
    all_db_path = (path.db.star, path.db.nm, path.db.hd, path.db.mx, path.db.ex, path.db.club, path.db.mission)

    # extract all djnames and disc/club/mission names
    all_dj = set()
    all_name = dict()
    for mode, directory in zip(all_type, all_db_path):
        all_name[mode] = extract(directory)

    # convert the set into a dictionary indexable by djname
    all_dj = {dj[0]: dict(zip(("name", "icon"), (dj[0], dj[1]))) for dj in all_dj}

    # insert extracted names for each djname the dictionary
    for mode in all_name:
        for dj in all_dj:
            all_dj[dj][mode] = dict(all_name[mode])
    del all_name  # no longer needed

    # fill scores
    for mode, directory in zip(all_type, all_db_path):
        fill(mode, directory)

    # write dj index
    with open(path.index.dj, "wb") as f:
        f.write(json.dumps([{"id": zlib.crc32(dj.encode()), "name": dj} for dj in sorted(all_dj)], indent=1).encode())

    # write dj records
    while all_dj:
        key, value = all_dj.popitem()
        with open("{}{}.json".format(path.db.dj, zlib.crc32(key.encode())), "wb") as f:
            f.write(json.dumps(value, indent=1).encode())


def master():
    """Use the local DJ database to create the master score records."""
    pop_master = {}

    for mode in (game.mode.star, game.chart.nm["str"], game.chart.hd["str"], game.chart.mx["str"], game.chart.ex["str"], game.mode.club, game.mode.mission):
        master = []
        for record in ls(path.db.dj):
            with open(path.db.dj + record, "rb") as f:
                record = json.loads(f.read().decode())
            master_score = sum([v[1] for k, v in record[mode].items()])
            if master_score:
                master.append((record["icon"], record["name"], master_score))
            if mode in (game.chart.nm["str"], game.chart.hd["str"], game.chart.mx["str"], game.chart.ex["str"]):
                if record["name"] not in pop_master:
                    pop_master[record["name"]] = [record["icon"], record["name"], master_score]
                else:
                    pop_master[record["name"]][2] += master_score
        master = [[rank + 1, dj[0], dj[1], dj[2]] for rank, dj in enumerate(sorted(master, key=lambda x: x[2], reverse=True))]
        with open("{}{}.json".format(path.db.master, mode), "wb") as f:
            f.write(json.dumps({"ranking": master}, indent=1).encode())

    pop_master = [[rank + 1, dj[0], dj[1], dj[2]] for rank, dj in enumerate(sorted(pop_master.values(), key=lambda x: x[2], reverse=True))]
    with open("{}{}.json".format(path.db.master, "pop"), "wb") as f:
        f.write(json.dumps({"ranking": pop_master}, indent=1).encode())
