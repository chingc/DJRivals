"""Database creation."""
from collections import OrderedDict as dict
import json
import time
import zlib

from common import _, _clean, _list_dir, _make_dir
from ranking import ranking


def build(mode, name):
    """Build a local database of the specified mode and name.

    Any of the four game mode constants defined in the common module can be
    given as the first argument.  The name must be the complete name of a disc,
    disc set, or mission.

    """
    if mode == _.STAR:
        path  = _.STAR_INDEX
        level = [("nm", _.STAR_DB_DIR)]
    elif mode == _.POP:
        path  = _.POP_INDEX
        level = [
            ("nm", _.POP_NM_DB_DIR),
            ("hd", _.POP_HD_DB_DIR),
            ("mx", _.POP_MX_DB_DIR),
            ("ex", _.POP_EX_DB_DIR)
        ]
    elif mode == _.CLUB:
        path  = _.CLUB_INDEX
        level = [("nm", _.CLUB_DB_DIR)]
    elif mode == _.MISSION:
        path  = _.MISSION_INDEX
        level = [("nm", _.MISSION_DB_DIR)]
    else:
        raise ValueError("invalid game mode")
    for mode_str, db_dir in level:
        results = ranking(mode, name, _.CHART[mode_str])
        if len(results) == 0:
            continue
        clean_name = _clean(name)
        data = dict()
        data["name"] = name
        data["eyecatch"] = "{}.png".format(clean_name)
        data["icon"] = "{}_{}.png".format(clean_name, _.CHART[mode_str])
        data["ranking"] = results
        with open("{}{}.json".format(db_dir, clean_name), "wb") as f:
            f.write(json.dumps(data, indent=2).encode())
        print('Wrote: "{}{}.json"'.format(db_dir, clean_name))
    with open(path, "rb") as f:
        data = json.loads(f.read().decode(), object_pairs_hook=dict)
        data[name]["timestamp"] = int(time.time())
    with open(path, "wb") as f:
        f.write(json.dumps(data, indent=2).encode())


def dj():
    """Build a DJ database using information from the local database.

    """
    def _extract(dj_set, directory):
        """Extract DJ and name data."""
        names = dict()
        for json_file in _list_dir(directory):
            with open(directory + json_file, "rb") as f:
                data = json.loads(f.read().decode())
            dj_set.update([(record[1], record[2]) for record in data["ranking"]])
            names[data["name"]] = [9999, 0]
        return names

    def _fill(dj_dict, directory, mode):
        """Fill in scores for each DJ."""
        for json_file in _list_dir(directory):
            with open(directory + json_file, "rb") as f:
                data = json.loads(f.read().decode())
            for record in data["ranking"]:
                dj_dict[record[2]][mode]["scores"][data["name"]] = [record[0], record[3]]

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
            djs[dj][mode] = dict()
            djs[dj][mode]["scores"] = dict(extracted[mode])
            djs[dj][mode]["master"] = [9999, 0]

    # fill in scores
    _fill(djs, _.STAR_DB_DIR, "star")
    _fill(djs, _.POP_NM_DB_DIR, "pop_nm")
    _fill(djs, _.POP_HD_DB_DIR, "pop_hd")
    _fill(djs, _.POP_MX_DB_DIR, "pop_mx")
    _fill(djs, _.POP_EX_DB_DIR, "pop_ex")
    _fill(djs, _.CLUB_DB_DIR, "club")
    _fill(djs, _.MISSION_DB_DIR, "mission")

    # convert score dictionaries to lists
    for mode in extracted:
        for dj in djs:
            djs[dj][mode]["scores"] = [(name, score[0], score[1]) for name, score in djs[dj][mode]["scores"].items()]

    # calculate and fill master scores
    for mode in extracted:
        extracted[mode] = sorted(filter(lambda x: x[1] > 0, [(dj, sum([score[2] for score in djs[dj][mode]["scores"]])) for dj in djs]), key=lambda x: x[1], reverse=True)
        for rank, score in enumerate(extracted[mode]):
            djs[score[0]][mode]["master"] = [rank + 1, score[1]]

    # write DJ files and index
    for k, v in djs.items():
        with open("{}{}.json".format(_.DJ_DB_DIR, zlib.crc32(k.encode())), "wb") as f:
            f.write(json.dumps(v, indent=2).encode())
    with open(_.DJ_INDEX, "wb") as f:
        f.write(json.dumps([{"id": zlib.crc32(dj.encode()), "name": dj} for dj in sorted(djs.keys())], indent=2).encode())


def master():
    """Build a master score database using information from the local database.

    The database is implemented as a collection of JSON files.  One JSON file is
    created for each game mode (except Crew Race).

    """
    dj_db_dir = _make_dir(_.DJ_DB_DIR)
    master_db_dir = _make_dir(_.MASTER_DB_DIR)
    results = {"star": [], "pop": [], "club": [], "mission": []}
    print("Writing master ranking files...")
    for json_file in _list_dir(dj_db_dir):
        with open(dj_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        for mode in ["star", "pop", "club", "mission"]:
            results[mode].append([data[mode]["master"][0], data["icon"], data["name"], data[mode]["master"][1]])
    for mode in ["star", "pop", "club", "mission"]:
        results[mode].sort()
        with open(master_db_dir + mode + ".json", "wb") as f:
            f.write(json.dumps({"ranking": results[mode]}, indent=1).encode())


_make_dir(_.DJ_DB_DIR)
_make_dir(_.STAR_DB_DIR)
_make_dir(_.POP_NM_DB_DIR)
_make_dir(_.POP_HD_DB_DIR)
_make_dir(_.POP_MX_DB_DIR)
_make_dir(_.POP_EX_DB_DIR)
_make_dir(_.CLUB_DB_DIR)
_make_dir(_.MISSION_DB_DIR)
