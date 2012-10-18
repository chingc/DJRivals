"""Image retrieval."""
import json

from common import _, _clean, _exists, _list_dir, _make_dir, _open_url


def image(mode):
    """Download disc, disc set, and mission icons from the DJMAX site.

    An icon will be skipped if it is determined that it already exists.
    Existence is checked by a simple path check.

    """
    if mode == _.STAR:
        id_url  = _.STAR_ID_URL
        img_url = _.DISC_IMAGE_URL
        img_dir = _.DISC_IMAGE_DIR
        keys    = _.DISC_KEY
        last    = _.STAR_PAGES
        suffix  = 2
    elif mode == _.POP:
        id_url  = _.POP_ID_URL
        img_url = _.DISC_IMAGE_URL
        img_dir = _.DISC_IMAGE_DIR
        keys    = _.DISC_KEY
        last    = _.POP_PAGES
        suffix  = 5
    elif mode == _.CLUB:
        id_url  = _.CLUB_ID_URL
        img_url = _.CLUB_IMAGE_URL
        img_dir = _.CLUB_IMAGE_DIR
        keys    = _.CLUB_KEY
        last    = _.CLUB_PAGES
        suffix  = 2
    elif mode == _.MISSION:
        id_url  = _.MISSION_ID_URL
        img_url = _.MISSION_IMAGE_URL
        img_dir = _.MISSION_IMAGE_DIR
        keys    = _.MISSION_KEY
        last    = _.MISSION_PAGES
        suffix  = 2
    else:
        raise ValueError("invalid game mode")
    for page in range(1, last + 1):
        data = json.loads(_open_url(id_url.format(page), "retrieving image name").read().decode())["DATA"]["RECORD"]
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
                    f.write(_open_url(img_url.format(theirname), "downloading image").read())
                print('Wrote: "{}{}"'.format(img_dir, myname))


def icon():
    """Download DJ icons from the DJMAX site.

    Scans the local database and downloads the necessary DJ icons.  An icon will
    be skipped if it is determined that it already exists.  Existence is checked
    by a simple path check.

    """
    icons = set()
    for directory in [_.STAR_DB_DIR, _.POP_NM_DB_DIR, _.POP_HD_DB_DIR, _.POP_MX_DB_DIR, _.POP_EX_DB_DIR, _.CLUB_DB_DIR, _.MISSION_DB_DIR]:
        for json_file in _list_dir(directory):
            with open(directory + json_file, "rb") as f:
                data = json.loads(f.read().decode())
            icons.update([record[1] for record in data["ranking"]])
    for icon in icons:
        if _exists(_.ICON_IMAGE_DIR + icon):
            continue
        with open(_.ICON_IMAGE_DIR + icon, "wb") as f:
            f.write(_open_url(_.ICON_IMAGE_URL.format(icon), "downloading DJ icon").read())
        print('Wrote: "{}{}"'.format(_.ICON_IMAGE_DIR, icon))


_make_dir(_.DISC_IMAGE_DIR)
_make_dir(_.CLUB_IMAGE_DIR)
_make_dir(_.MISSION_IMAGE_DIR)
_make_dir(_.ICON_IMAGE_DIR)
_make_dir(_.STAR_DB_DIR)
_make_dir(_.POP_NM_DB_DIR)
_make_dir(_.POP_HD_DB_DIR)
_make_dir(_.POP_MX_DB_DIR)
_make_dir(_.POP_EX_DB_DIR)
_make_dir(_.CLUB_DB_DIR)
_make_dir(_.MISSION_DB_DIR)
