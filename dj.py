"""DJ database creation."""
from collections import OrderedDict
import json
import time
import zlib

from common import _dir_listing, _link, _make_dir


def database():
    """database() -> None

    Create a DJ database using information in the local database.  The database
    is implemented as a collection of JSON files.  One JSON file is created for
    each DJ.  Refer to data_structures.txt for the format and contents of these
    files.

    """
    start_time = time.time()
    pop_db_dir = _make_dir(_link("pop_database_directory"))
    dj_db_dir = _make_dir(_link("dj_database_directory"))
    dj_index_file = _link("dj_index_file")
    db_contents = _dir_listing(pop_db_dir)
    djs = set()
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
            djs = djs.union([record[2] for record in data[chart]["ranking"]])
            if data[chart]["difficulty"]:
                disc_list[chart][data["name"]] = 0
    djs = {dj: OrderedDict([("name", dj), ("pop", OrderedDict((chart, dict(disc_list[chart])) for chart in charts))]) for dj in djs}
    for json_file in db_contents:
        with open(pop_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        for chart in charts:
            for record in data[chart]["ranking"]:
                djs[record[2]]["pop"][chart][data["name"]] = record[3]
    for chart in charts:
        for dj in djs:
            djs[dj]["pop"][chart] = sorted(djs[dj]["pop"][chart].items())
    for k, v in djs.items():
        with open("{}{}.json".format(dj_db_dir, zlib.crc32(k.encode())), "wb") as f:
            f.write(json.dumps(v).encode())
    with open(dj_index_file, "wb") as f:
        f.write(json.dumps([{"id": zlib.crc32(dj.encode()), "name": dj} for dj in djs.keys()]).encode())
    elapsed_time = round(time.time() - start_time)
    print("Database creation took {} seconds.".format(elapsed_time))
