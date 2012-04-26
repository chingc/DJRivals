"""Master ranking database creation."""
import json

from common import _dir_listing, _link, _make_dir


def database():
    """database() -> None

    Create the master ranking database using information in the local database.
    The database is implemented as a collection of JSON files.  One JSON file is
    created for each game mode (except Crew Race).  Refer to data_structures.txt
    for the format and contents of these files.

    """
    dj_db_dir = _make_dir(_link("dj_database_directory"))
    master_db_dir = _make_dir(_link("master_database_directory"))
    results = []
    print("Writing master ranking files...")
    for json_file in _dir_listing(dj_db_dir):
        with open(dj_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        results.append([data["pop"]["master"][0], data["icon"], data["name"], data["pop"]["master"][1]])
    results.sort()
    with open(master_db_dir + "pop.json", "wb") as f:
        f.write(json.dumps(results).encode())
