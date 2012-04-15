"""DJ database creation."""
from collections import OrderedDict
import json
import time

from common import _dir_listing, _link, _make_dir


def _clean_name(name):
    """Sanitize DJ names."""
    if name.find("*") > -1: name = name.replace("*", "(8)")
    if name.find("/") > -1: name = name.replace("/", "(fs)")
    if name.find("?") > -1: name = name.replace("?", "(qm)")
    if name.find(":") > -1: name = name.replace(":", "(;)")
    if name.lower().startswith("con"): name = "(-)" + name   # i never knew this
    return name


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
    db_contents = _dir_listing(pop_db_dir)
    dj = set()
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
        dj = dj.union([(_clean_name(record[2]), record[2]) for chart in charts for record in data["ranking"][chart]])
        for chart in charts:
            if data["difficulty"][chart]:
                disc_list[chart][data["name"]["full"]] = 0
    with open(dj_db_dir + "!__all_djnames__.json", "wb") as f:
        f.write(json.dumps(sorted([name[1] for name in dj])).encode())
    dj = {name[0]: OrderedDict({"full": name[1]}) for name in dj}
    for name in dj:
        dj[name]["pop"] = OrderedDict()
        for chart in charts:
            dj[name]["pop"][chart] = dict(disc_list[chart])
    for json_file in db_contents:
        with open(pop_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        for chart in charts:
            for result in data["ranking"][chart]:
                name = _clean_name(result[2])
                if name in dj:
                    dj[name]["pop"][chart][data["name"]["full"]] = result[3]
    for name in dj:
        for chart in charts:
            dj[name]["pop"][chart] = sorted(dj[name]["pop"][chart].items())
    for k, v in dj.items():
        with open(dj_db_dir + k + ".json", "wb") as f:
            f.write(json.dumps(v).encode())
    elapsed_time = round(time.time() - start_time)
    print("Database creation took {} seconds.".format(elapsed_time))
