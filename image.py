"""Image retrieval."""
import json

from common import clean, exists, ls, urlopen_image, urlopen_json
from settings import path, site, url


def disc():
    """Download disc, disc set, and mission icons from the DJMAX site.

    An icon will be skipped if it is determined that it already exists.
    Existence is checked by a simple path check.

    """
    all_id_urls  = (url.id.star, url.id.pop, url.id.club, url.id.mission)
    all_img_urls = (url.img.star, url.img.pop, url.img.club, url.img.mission)
    all_img_dirs = (path.img.star, path.img.pop, path.img.club, path.img.mission)
    all_keys     = (site.key.star, site.key.pop, site.key.club, site.key.mission)
    all_pages    = (site.pages.star, site.pages.pop, site.pages.club, site.pages.mission)
    all_suffixes = (1, 4, 1, 1)  # image suffix ranges

    for id_url, img_url, img_dir, key, end, suffix in zip(all_id_urls, all_img_urls, all_img_dirs, all_keys, all_pages, all_suffixes):
        images = []
        for page in range(1, end + 1):
            for record in urlopen_json(id_url.format(page), "Retrieving image name"):
                images.append((record[key["image"]] + (".png" if key == site.key.mission else ""), clean(record[key["name"]])))
        for image in images:
            unclean_name = image[0]
            name, ext = image[0].rsplit(".", 1)
            for i in range(1, suffix + 1):
                clean_name = "{}_{}.{}".format(image[1], i, ext)
                if exists(img_dir + clean_name):
                    continue
                if key == site.key.pop:
                    unclean_name = "{}{}.{}".format(name[:-1], i, ext)
                with open(img_dir + clean_name, "wb") as f:
                    f.write(urlopen_image(img_url.format(unclean_name)))
                print('Wrote: "{}{}"'.format(img_dir, clean_name))


def icon():
    """Download DJ icons from the DJMAX site.

    Scans the local database and downloads the necessary DJ icons.  An icon will
    be skipped if it is determined that it already exists.  Existence is checked
    by a simple path check.

    """
    icons = set()
    for db in (path.db.star, path.db.nm, path.db.hd, path.db.mx, path.db.ex, path.db.club, path.db.mission):
        for record in ls(db):
            with open(db + record, "rb") as f:
                data = json.loads(f.read().decode())
            icons.update([dj["djicon"] for dj in data["ranking"]])
    for icon in icons:
        if exists(path.img.icon + icon):
            continue
        with open(path.img.icon + icon, "wb") as f:
            f.write(urlopen_image(url.img.icon.format(icon)))
        print('Wrote: "{}{}"'.format(path.img.icon, icon))
