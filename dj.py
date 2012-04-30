"""DJ database creation."""
import json
import zlib

from common import _dir_listing, _link, _make_dir


def database():
    """database() -> None

    Create a DJ database using information in the local database.  The database
    is implemented as a collection of JSON files.  One JSON file is created for
    each DJ.  Refer to data_structures.txt for the format and contents of these
    files.

    """
    pop_db_dir = _make_dir(_link("pop_database_directory"))
    dj_db_dir = _make_dir(_link("dj_database_directory"))
    dj_index_file = _link("dj_index_file")
    db_contents = _dir_listing(pop_db_dir)
    djs = set()
    pop_master = []
    charts = ["nm", "hd", "mx"]
    disc_list = {
        "nm": {},
        "hd": {},
        "mx": {}
    }
    print("Writing DJ files...")
    for json_file in db_contents:
        with open(pop_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        for chart in charts:
            djs = djs.union([(record[1], record[2]) for record in data[chart]["ranking"]])
            if data[chart]["records"]:
                disc_list[chart][data["name"]] = [9999, 0]
    djs = {dj[1]: dict([("name", dj[1]), ("icon", dj[0])] + [("pop", {chart: dict(disc_list[chart]) for chart in charts})]) for dj in djs}
    for json_file in db_contents:
        with open(pop_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        for chart in charts:
            for record in data[chart]["ranking"]:
                djs[record[2]]["pop"][chart][data["name"]] = [record[0], record[3]]
    for dj in djs:
        total = 0
        for chart in charts:
            djs[dj]["pop"][chart] = sorted([(k, v[0], v[1]) for k, v in djs[dj]["pop"][chart].items()])
            total += sum([data[2] for data in djs[dj]["pop"][chart]])
        pop_master.append([dj, total])
    pop_master.sort(key=lambda x: x[1], reverse=True)
    for i, v in enumerate(pop_master):
        djs[v[0]]["pop"]["master"] = [i + 1, v[1]]
    for k, v in djs.items():
        with open("{}{}.json".format(dj_db_dir, zlib.crc32(k.encode())), "wb") as f:
            f.write(json.dumps(v).encode())
    with open(dj_index_file, "wb") as f:
        f.write(json.dumps([{"id": zlib.crc32(dj.encode()), "name": dj} for dj in sorted(djs.keys())]).encode())
