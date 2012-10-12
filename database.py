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
        level = [("nm", _make_dir(_.STAR_DB_DIR))]
    elif mode == _.POP:
        path  = _.POP_INDEX
        level = [("nm", _make_dir(_.POP_NM_DB_DIR)),
                 ("hd", _make_dir(_.POP_HD_DB_DIR)),
                 ("mx", _make_dir(_.POP_MX_DB_DIR)),
                 ("ex", _make_dir(_.POP_EX_DB_DIR))]
    elif mode == _.CLUB:
        path  = _.CLUB_INDEX
        level = [("nm", _make_dir(_.CLUB_DB_DIR))]
    elif mode == _.MISSION:
        path  = _.MISSION_INDEX
        level = [("nm", _make_dir(_.MISSION_DB_DIR))]
    else:
        raise ValueError("invalid game mode")
    for a, b in level:
        results = ranking(mode, name, _.CHART[a])
        if len(results) == 0:
            continue
        clean_name = _clean(name)
        data = dict()
        data["name"] = name
        data["eyecatch"] = "{}.png".format(clean_name)
        data["icon"] = "{}_{}.png".format(clean_name, _.CHART[a])
        data["ranking"] = results
        with open("{}{}.json".format(b, clean_name), "wb") as f:
            f.write(json.dumps(data, indent=2).encode())
        print('Wrote: "{}{}.json"'.format(b, clean_name))
    with open(path, "rb") as f:
        data = json.loads(f.read().decode(), object_pairs_hook=dict)
        data[name]["timestamp"] = int(time.time())
    with open(path, "wb") as f:
        f.write(json.dumps(data, indent=2).encode())


def dj():
    """Build a DJ database using information from the local database.

    The database is implemented as a collection of JSON files.  One JSON file is
    created for each DJ.

    """
    # todo: code cleanup
    def _dj_struct(name, icon, star, pop, club, mission):
        dj = OrderedDict()
        dj["name"] = name
        dj["icon"] = icon
        dj["star"] = OrderedDict()
        dj["star"]["scores"] = OrderedDict(star)
        dj["star"]["master"] = []
        dj["pop"] = OrderedDict()
        dj["pop"]["nm"] = OrderedDict(pop["nm"])
        dj["pop"]["hd"] = OrderedDict(pop["hd"])
        dj["pop"]["mx"] = OrderedDict(pop["mx"])
        dj["pop"]["ex"] = OrderedDict(pop["ex"])
        dj["pop"]["master"] = []
        dj["club"] = OrderedDict()
        dj["club"]["scores"] = OrderedDict(club)
        dj["club"]["master"] = []
        dj["mission"] = OrderedDict()
        dj["mission"]["scores"] = OrderedDict(mission)
        dj["mission"]["master"] = []
        return dj

    dj_db_dir      = _make_dir(_.DJ_DB_DIR)
    star_db_dir    = _make_dir(_.STAR_DB_DIR)
    pop_db_dir     = _make_dir(_.POP_DB_DIR)
    club_db_dir    = _make_dir(_.CLUB_DB_DIR)
    mission_db_dir = _make_dir(_.MISSION_DB_DIR)

    star_dir_list    = _list_dir(star_db_dir)
    pop_dir_list     = _list_dir(pop_db_dir)
    club_dir_list    = _list_dir(club_db_dir)
    mission_dir_list = _list_dir(mission_db_dir)

    djs     = set()
    star    = OrderedDict()
    pop     = {"nm": OrderedDict(), "hd": OrderedDict(), "mx": OrderedDict(), "ex": OrderedDict()}
    club    = OrderedDict()
    mission = OrderedDict()

    star_master    = []
    pop_master     = []
    club_master    = []
    mission_master = []

    print("Writing DJ files...")

    # gather a list of all DJ names and all rankings that have at least one record
    for json_file in star_dir_list:
        with open(star_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        djs = djs.union([(record[1], record[2]) for record in data["ranking"]])
        if data["records"]:
            star[data["name"]] = [9999, 0]
    for json_file in pop_dir_list:
        with open(pop_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        for chart in _.CHARTS:
            djs = djs.union([(record[1], record[2]) for record in data[chart]["ranking"]])
            if data[chart]["records"]:
                pop[chart][data["name"]] = [9999, 0]
    for json_file in club_dir_list:
        with open(club_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        djs = djs.union([(record[1], record[2]) for record in data["ranking"]])
        if data["records"]:
            club[data["name"]] = [9999, 0]
    for json_file in mission_dir_list:
        with open(mission_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        djs = djs.union([(record[1], record[2]) for record in data["ranking"]])
        if data["records"]:
            mission[data["name"]] = [9999, 0]

    # convert the DJ names set into a dictionary
    djs = {dj[1]: _dj_struct(dj[1], dj[0], star, pop, club, mission) for dj in djs}

    # fill in scores
    for json_file in star_dir_list:
        with open(star_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        for record in data["ranking"]:
            djs[record[2]]["star"]["scores"][data["name"]] = [record[0], record[3]]
    for json_file in pop_dir_list:
        with open(pop_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        for chart in _.CHARTS:
            for record in data[chart]["ranking"]:
                djs[record[2]]["pop"][chart][data["name"]] = [record[0], record[3]]
    for json_file in club_dir_list:
        with open(club_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        for record in data["ranking"]:
            djs[record[2]]["club"]["scores"][data["name"]] = [record[0], record[3]]
    for json_file in mission_dir_list:
        with open(mission_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        for record in data["ranking"]:
            djs[record[2]]["mission"]["scores"][data["name"]] = [record[0], record[3]]

    # convert dictionaries to lists and obtain master scores
    for dj in djs:
        star_total    = 0
        pop_total     = 0
        club_total    = 0
        mission_total = 0
        djs[dj]["star"]["scores"] = sorted([(k, v[0], v[1]) for k, v in djs[dj]["star"]["scores"].items()])
        star_total = sum([data[2] for data in djs[dj]["star"]["scores"]])
        for chart in _.CHARTS:
            djs[dj]["pop"][chart] = sorted([(k, v[0], v[1]) for k, v in djs[dj]["pop"][chart].items()])
            pop_total += sum([data[2] for data in djs[dj]["pop"][chart]])
        djs[dj]["club"]["scores"] = sorted([(k, v[0], v[1]) for k, v in djs[dj]["club"]["scores"].items()])
        club_total = sum([data[2] for data in djs[dj]["club"]["scores"]])
        djs[dj]["mission"]["scores"] = sorted([(k, v[0], v[1]) for k, v in djs[dj]["mission"]["scores"].items()])
        mission_total = sum([data[2] for data in djs[dj]["mission"]["scores"]])
        star_master.append([dj, star_total])
        pop_master.append([dj, pop_total])
        club_master.append([dj, club_total])
        mission_master.append([dj, mission_total])
    star_master.sort(key=lambda x: x[1], reverse=True)
    pop_master.sort(key=lambda x: x[1], reverse=True)
    club_master.sort(key=lambda x: x[1], reverse=True)
    mission_master.sort(key=lambda x: x[1], reverse=True)

    # assign master scores
    for i, v in enumerate(star_master):
        djs[v[0]]["star"]["master"] = [i + 1, v[1]]
    for i, v in enumerate(pop_master):
        djs[v[0]]["pop"]["master"] = [i + 1, v[1]]
    for i, v in enumerate(club_master):
        djs[v[0]]["club"]["master"] = [i + 1, v[1]]
    for i, v in enumerate(mission_master):
        djs[v[0]]["mission"]["master"] = [i + 1, v[1]]

    # write the DJ files
    for k, v in djs.items():
        with open("{}{}.json".format(dj_db_dir, zlib.crc32(k.encode())), "wb") as f:
            f.write(json.dumps(v, indent=1).encode())

    # write the DJ index
    with open(_.DJ_INDEX, "wb") as f:
        f.write(json.dumps([{"id": zlib.crc32(dj.encode()), "name": dj} for dj in sorted(djs.keys())], indent=1).encode())


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
