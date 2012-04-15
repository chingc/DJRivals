"""Image retrieval."""
from urllib.request import urlopen
import json

from common import _clean, _dir_listing, _file_exists, _link, _make_dir


def discs():
    """discs() -> None

    Download all disc images from the DJMAX site.  An image will be skipped if
    it is determined that the file already exists.  Existence is checked using a
    simple filename lookup.

    """
    url = _link("pop_ranking_page_url")
    image_url = _link("disc_image_url")
    image_dir = _make_dir(_link("disc_image_directory"))
    for page in range(1, 9):
        data = json.loads(urlopen(url.format(page)).read().decode())["DATA"]["RECORD"]
        for record in data:
            i = record["DISCIMG"].rfind(".")
            name, extension = record["DISCIMG"][:i], record["DISCIMG"][i:]
            for chart in range(1, 5):
                theirname = "{}{}{}".format(name[:-1], chart, extension)
                myname = "{}_{}{}".format(_clean(record["DISCNAME"]), chart, extension)
                if _file_exists(image_dir + myname):
                    continue
                with open(image_dir + myname, "wb") as f:
                    f.write(urlopen(image_url.format(theirname)).read())
                print('Wrote: "{}{}"'.format(image_dir, myname))


def icons():
    """icons() -> None

    Examine the local database and download all necessary DJ icons from the
    DJMAX site.  An image will be skipped if it is determined that the file
    already exists.  Existence is checked using a simple filename lookup.

    """
    url = _link("icon_image_url")
    pop_db_dir = _make_dir(_link("pop_database_directory"))
    image_dir = _make_dir(_link("icon_image_directory"))
    icons = []
    for json_file in _dir_listing(pop_db_dir):
        with open(pop_db_dir + json_file, "rb") as f:
            ranking = json.loads(f.read().decode())["ranking"]
        icons.extend([result[1] for chart in ["nm", "hd", "mx"] for result in ranking[chart]])
    for icon in set(icons):
        if _file_exists(image_dir + icon):
            continue
        with open(image_dir + icon, "wb") as f:
            f.write(urlopen(url.format(icon)).read())
        print('Wrote: "{}{}"'.format(image_dir, icon))
