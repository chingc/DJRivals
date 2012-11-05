"""DJRivals database updater."""
import threading
import time

from common import _
import database
import html
import image
import index


def _update(mode, stop, lock):
    """Continuously update the specified database."""
    # the interval is used to prevent hammering the DJMAX site.  it sets the
    # number of seconds to wait before downloading score data again.
    if mode == _.STAR:
        interval = 900
    elif mode == _.POP:
        interval = 600
    elif mode == _.CLUB:
        interval = 1200
    elif mode == _.MISSION:
        interval = 1800
    else:
        raise ValueError("invalid game mode")
    while not stop.is_set():
        with lock:
            data = index.index(mode)
            next = sorted(data.keys(), key=lambda x: data[x]["timestamp"], reverse=True)[-1]
            index.touch_time(mode, next)
        database.build(mode, next)
        stop.wait(interval)


def update(threads=2):
    """Continuously update the databases."""
    stops = []
    for mode in (_.STAR, _.POP, _.CLUB, _.MISSION):
        run = threads
        lock = threading.Lock()
        while run > 0:
            stop = threading.Event()
            threading.Thread(target=_update, args=(mode, stop, lock)).start()
            stops.append(stop)
            run -= 1
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        for stop in stops:
            stop.set()
        print("Finishing current jobs.  Please wait...")
        while threading.active_count() > 1:
            time.sleep(2)
        print("Done.")


def indexes():
    """Update indexes."""
    for mode in (_.STAR, _.POP, _.CLUB, _.MISSION):
        index.index(mode, True)
        image.image(mode)
    print("Done.")


def sync():
    """Build the DJ database and front-end."""
    database.dj()
    image.icon()
    html.pages()
    print("Done.")
