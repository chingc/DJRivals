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
    # the cycle variable is used to prevent hammering the DJMAX site.  it sets
    # the minimum hours to take to update all databases within an index by a
    # single thread.  the actual time may exceed the specified cycle.  e.g. if
    # cycle is set to zero.  when multiple threads are used, the actual time
    # required to update all databases within an index is greater than or equal
    # to the cycle divided by the number of threads.
    if mode == _.STAR:
        cycle = 48
    elif mode == _.POP:
        cycle = 24
    elif mode == _.CLUB:
        cycle = 36
    elif mode == _.MISSION:
        cycle = 36
    else:
        raise ValueError("invalid game mode")
    while not stop.is_set():
        with lock:
            data = index.index(mode)
            next = sorted(data.keys(), key=lambda x: data[x]["timestamp"], reverse=True).pop()
            index.touch_time(mode, next)
        database.build(mode, next)
        stop.wait(cycle * 60 * 60 / len(data))


def update():
    """Continuously update the databases."""
    stop = threading.Event()
    for mode in (_.STAR, _.POP, _.CLUB, _.MISSION):
        lock = threading.Lock()
        threading.Thread(target=_update, args=(mode, stop, lock)).start()
        threading.Thread(target=_update, args=(mode, stop, lock)).start()
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
        image.image(mode)
    print("Done.")


def finish():
    """Build the DJ database and html index."""
    database.dj()
    image.icon()
    html.index()
    print("Done.")
