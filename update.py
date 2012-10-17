"""DJRivals database updater."""
import threading
import time

from common import _
import database
import html
import image
import index


def _update(name, mode, stop):
    """Continuously update the specified database."""
    if mode == _.STAR:
        hours = 36
    elif mode == _.POP:
        hours = 20
    elif mode == _.CLUB:
        hours = 12
    elif mode == _.MISSION:
        hours = 12
    else:
        raise ValueError("invalid game mode")
    while not stop.is_set():
        data = index.index(mode)
        wait = (hours * 60 * 60 / len(data))
        next = sorted(data.keys(), key=lambda x: data[x]["timestamp"], reverse=True).pop()
        database.build(mode, next)
        stop.wait(wait)
    print(name, "thread stopped.")


def update():
    """Continuously update the databases."""
    stop = threading.Event()
    for mode_str, mode in (("Star", _.STAR), ("Pop", _.POP), ("Club", _.CLUB), ("Mission", _.MISSION)):
        threading.Thread(target=_update, args=(mode_str, mode, stop)).start()
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        stop.set()
        print("Finishing current jobs.  Please wait...")
        while threading.active_count() > 1:
            time.sleep(2)
        print("Done.")


def indexes():
    """Update indexes."""
    for mode in (_.STAR, _.POP, _.CLUB, _.MISSION):
        index.index(mode, True)


def images():
    """Retrieve new images, if any."""
    for mode in (_.STAR, _.POP, _.CLUB, _.MISSION):
        image.image(mode)
    image.icon()


def finish():
    """Build the DJ database and html index."""
    database.dj()
    images()
    html.index()
    print("Done.")
