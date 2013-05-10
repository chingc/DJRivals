"""Database creation."""
from collections import OrderedDict as dict
import json
import zlib

from common import clean, ls, mkdir
from settings import game, path
import ranking
#from common import _, _clean, _list_dir, _make_dir
#from ranking import ranking


def create(mode, name):
    """Create a local database of the specified mode and name.

    Arguments:
    mode -- One of the four game modes.
    name -- The full name of a disc, disc set, or mission.

    """
    if mode == game.mode.star: level = [(game.chart.nm, path.db.star)]
    elif mode == game.mode.pop: level = zip(game.chart.all, path.db.pop)
    elif mode == game.mode.club: level = [(game.chart.nm, path.db.club)]
    elif mode == game.mode.mission: level = [(game.chart.nm, path.db.mission)]
    else: raise ValueError("Invalid game mode")
    for chart, directory in level:
        results = ranking.get(mode, name, chart)
        if results:
            clean_name = clean(name)
            db = dict()
            db["name"] = name
            db["eyecatch"] = "{}.png".format(clean_name)
            db["icon"] = "{}_{}.png".format(clean_name, chart["int"])
            db["ranking"] = results
            with open(directory + clean_name + ".json", "wb") as f:
                f.write(json.dumps(db, indent=1).encode())
            print('Wrote: "{}{}.json"'.format(directory, clean_name))


def dj():
    """Create a database of scores for each DJ using the local database."""
    def _extract(dj_set, directory):
        """Extract DJ and name data."""
        names = dict()
        for json_file in _list_dir(directory):
            with open(directory + json_file, "rb") as f:
                data = json.loads(f.read().decode())
            dj_set.update((record[1], record[2]) for record in data["ranking"])
            names[data["name"]] = [9999, 0]
        names["_master_"] = [9999, 0]
        return names

    def _fill(dj_dict, directory, mode):
        """Fill scores for each DJ."""
        for json_file in _list_dir(directory):
            with open(directory + json_file, "rb") as f:
                data = json.loads(f.read().decode())
            for record in data["ranking"]:
                dj_dict[record[2]][mode][data["name"]] = [record[0], record[3]]

    djs = set()

    # extract disc, disc set, and mission names
    extracted = dict([
        ("star", _extract(djs, _.STAR_DB_DIR)),
        ("pop_nm", _extract(djs, _.POP_NM_DB_DIR)),
        ("pop_hd", _extract(djs, _.POP_HD_DB_DIR)),
        ("pop_mx", _extract(djs, _.POP_MX_DB_DIR)),
        ("pop_ex", _extract(djs, _.POP_EX_DB_DIR)),
        ("club", _extract(djs, _.CLUB_DB_DIR)),
        ("mission", _extract(djs, _.MISSION_DB_DIR))
    ])

    # convert the DJ set into a dictionary
    djs = {dj[1]: dict([("name", dj[1]), ("icon", dj[0])]) for dj in djs}

    # insert extracted into the DJ set
    for mode in extracted:
        for dj in djs:
            djs[dj][mode] = dict(extracted[mode])

    # fill scores
    _fill(djs, _.STAR_DB_DIR, "star")
    _fill(djs, _.POP_NM_DB_DIR, "pop_nm")
    _fill(djs, _.POP_HD_DB_DIR, "pop_hd")
    _fill(djs, _.POP_MX_DB_DIR, "pop_mx")
    _fill(djs, _.POP_EX_DB_DIR, "pop_ex")
    _fill(djs, _.CLUB_DB_DIR, "club")
    _fill(djs, _.MISSION_DB_DIR, "mission")

    # calculate, fill, and write master scores
    for mode in extracted:
        extracted[mode] = filter(lambda x: x[2] > 0, ((djs[dj]["icon"], dj, sum(score[1] for score in djs[dj][mode].values())) for dj in djs))
        extracted[mode] = [(rank + 1, info[0], info[1], info[2]) for rank, info in enumerate(sorted(extracted[mode], key=lambda x: x[2], reverse=True))]
        for info in extracted[mode]:
            djs[info[2]][mode]["_master_"] = [info[0], info[3]]
        with open(_.MASTER_DB_DIR + mode + ".json", "wb") as f:
            f.write(json.dumps({"ranking": extracted[mode]}, indent=None).encode())

    # write pop master (overall) scores
    for mode in ["star", "club", "mission"]:
        del extracted[mode]
    extracted = sorted(([info[1], info[2], info[3]] for mode in extracted for info in extracted[mode]), key=lambda x: x[1])
    try:
        pop = [extracted.pop()]
    except IndexError:
        pass
    else:
        while len(extracted) > 0:
            next = extracted.pop()
            if next[1] == pop[-1][1]:
                pop[-1][2] += next[2]
            else:
                pop.append(next)
        pop = [(rank + 1, score[0], score[1], score[2]) for rank, score in enumerate(sorted(pop, key=lambda x: x[2], reverse=True))]
        with open(_.MASTER_DB_DIR + "pop.json", "wb") as f:
            f.write(json.dumps({"ranking": pop}, indent=None).encode())

    # write DJ files and index
    for dj, scores in djs.items():
        with open("{}{}.json".format(_.DJ_DB_DIR, zlib.crc32(dj.encode())), "wb") as f:
            f.write(json.dumps(scores, indent=None).encode())
    with open(_.DJ_INDEX, "wb") as f:
        f.write(json.dumps([{"id": zlib.crc32(dj.encode()), "name": dj} for dj in sorted(djs.keys())], indent=None).encode())
