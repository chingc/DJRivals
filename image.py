"""Image retrieval."""
from urllib.request import urlopen
import json

from common import _, _clean, _exists, _list_dir, _make_dir


def icon():
    """Download all necessary DJ icons from the DJMAX site.

    An image will be skipped if it is determined that the file already exists.
    Existence is checked using a simple filename lookup.

    """
    url = _.ICON_IMAGE_URL
    image_dir      = _make_dir(_.ICON_IMAGE_DIR)
    star_db_dir    = _make_dir(_.STAR_DB_DIR)
    pop_db_dir     = _make_dir(_.POP_DB_DIR)
    club_db_dir    = _make_dir(_.CLUB_DB_DIR)
    mission_db_dir = _make_dir(_.MISSION_DB_DIR)
    icons = set()
    for directory in [star_db_dir, club_db_dir, mission_db_dir]:
        for json_file in _list_dir(directory):
            with open(directory + json_file, "rb") as f:
                data = json.loads(f.read().decode())
            icons = icons.union([record[1] for record in data["ranking"]])
    for json_file in _list_dir(pop_db_dir):
        with open(pop_db_dir + json_file, "rb") as f:
            data = json.loads(f.read().decode())
        icons = icons.union([record[1] for chart in ["nm", "hd", "mx"] for record in data[chart]["ranking"]])
    for icon in icons:
        if _exists(image_dir + icon):
            continue
        with open(image_dir + icon, "wb") as f:
            f.write(urlopen(url.format(icon)).read())
        print('Wrote: "{}{}"'.format(image_dir, icon))


def mode(mode):
    """Download all images of the specified mode from the DJMAX site.

    An image will be skipped if it is determined that the file already exists.
    Existence is checked using a simple filename lookup.

    """
    if mode == _.STAR:
        id_url   = _.STAR_ID_URL
        img_url  = _.DISC_IMAGE_URL
        img_dir  = _make_dir(_.DISC_IMAGE_DIR)
        stop     = _.STAR_PAGES
        keys     = _.DISC_KEYS
        suffix   = 2
    elif mode == _.POP:
        id_url   = _.POP_ID_URL
        img_url  = _.DISC_IMAGE_URL
        img_dir  = _make_dir(_.DISC_IMAGE_DIR)
        stop     = _.POP_PAGES
        keys     = _.DISC_KEYS
        suffix   = 5
    elif mode == _.CLUB:
        id_url   = _.CLUB_ID_URL
        img_url  = _.CLUB_IMAGE_URL
        img_dir  = _make_dir(_.CLUB_IMAGE_DIR)
        stop     = _.CLUB_PAGES
        keys     = _.CLUB_KEYS
        suffix   = 2
    elif mode == _.MISSION:
        id_url   = _.MISSION_ID_URL
        img_url  = _.MISSION_IMAGE_URL
        img_dir  = _make_dir(_.MISSION_IMAGE_DIR)
        stop     = _.MISSION_PAGES
        keys     = _.MISSION_KEYS
        suffix   = 2
    else:
        raise ValueError("invalid argument")
    for page in range(1, stop + 1):
        data = json.loads(urlopen(id_url.format(page)).read().decode())["DATA"]["RECORD"]
        for record in data:
            theirname = record[keys["image"]] + (".png" if mode == _.MISSION else "")
            i = theirname.rfind(".")
            name, extension = theirname[:i], theirname[i:]
            for i in range(1, suffix):
                myname = "{}_{}{}".format(_clean(record[keys["name"]]), i, extension)
                if _exists(img_dir + myname):
                    continue
                if mode == _.POP:
                    theirname = "{}{}{}".format(name[:-1], i, extension)
                with open(img_dir + myname, "wb") as f:
                    f.write(urlopen(img_url.format(theirname)).read())
                print('Wrote: "{}{}"'.format(img_dir, myname))
