"""DJRivals database updater."""
import threading
import time

from settings import game
import database
#import html
import image
import index


def db(threads=2):
    """Continuously update the databases."""
    def oldest_last(mode):
        data = index.read()
        return sorted(data[mode].keys(), key=lambda x: data[mode][x]["timestamp"], reverse=True)

    def thread(mode, stop, lock):
        # the interval is used to prevent hammering the DJMAX site.  it sets the
        # number of seconds to wait before downloading score data again.
        if mode == game.mode.star: interval = 900
        elif mode == game.mode.pop: interval = 600
        elif mode == game.mode.club: interval = 1200
        elif mode == game.mode.mission: interval = 1800
        else: raise ValueError("Invalid game mode")
        while not stop.is_set():
            with lock:
                next = names[mode].pop()
            try:
                database.create(mode, next)
            except:
                names[mode].append(next)
                stop.set()
                raise
            else:
                with lock:
                    names[mode].insert(0, next)
                    index.touch(mode, next)
                stop.wait(interval)

    names = {}
    names[game.mode.star]    = oldest_last(game.mode.star)
    names[game.mode.pop]     = oldest_last(game.mode.pop)
    names[game.mode.club]    = oldest_last(game.mode.club)
    names[game.mode.mission] = oldest_last(game.mode.mission)

    stops = []
    for mode in (game.mode.star, game.mode.pop, game.mode.club, game.mode.mission):
        lock = threading.Lock()
        for t in range(threads):
            stop = threading.Event()
            threading.Thread(target=thread, args=(mode, stop, lock)).start()
            stops.append(stop)
    try:
        while True:
            print("{} of {} threads running.".format(threading.active_count() - 1, threads * 4), end="\r")
            time.sleep(30)
    except KeyboardInterrupt:
        for stop in stops:
            stop.set()
        print("Finishing current jobs.  Please wait...")
        while threading.active_count() > 1:
            time.sleep(2)
        print("Done.")


def other():
    """Update the index and download any necessary images."""
    start_time = time.monotonic()
    index.create()
    print("Index built (took: {:.2f}s)".format(time.monotonic() - start_time))

    start_time = time.monotonic()
    image.disc()
    print("Disc icons downloaded (took: {:.2f}s)".format(time.monotonic() - start_time))

    start_time = time.monotonic()
    image.icon()
    print("DJ icons downloaded (took: {:.2f}s)".format(time.monotonic() - start_time))
    print("Done.")


def sync():
    """Build the DJ database and front-end."""
    database.dj()
    image.icon()
    #html.pages()
    print("Done.")
