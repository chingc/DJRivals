"""Update manager."""
import threading
import time

from settings import game
import database
import html
import image
import index


def db(threads=2):
    """Continuously update the databases."""
    def oldest_first(mode):
        idx = index.read()
        return sorted(idx[mode], key=lambda x: idx[mode][x]["timestamp"])

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
                next = names[mode].pop(0)
            try:
                database.create(mode, next)
            except:
                names[mode].insert(0, next)
                stop.set()
                raise
            else:
                with lock:
                    names[mode].append(next)
                    index.touch(mode, next)
                stop.wait(interval)

    names = {}
    names[game.mode.star]    = oldest_first(game.mode.star)
    names[game.mode.pop]     = oldest_first(game.mode.pop)
    names[game.mode.club]    = oldest_first(game.mode.club)
    names[game.mode.mission] = oldest_first(game.mode.mission)

    stops = []
    for mode in (game.mode.star, game.mode.pop, game.mode.club, game.mode.mission):
        lock = threading.Lock()
        for t in range(threads):
            stop = threading.Event()
            threading.Thread(target=thread, args=(mode, stop, lock)).start()
            stops.append(stop)
    try:
        while threading.active_count() > 1:
            print("{} of {} threads running.".format(threading.active_count() - 1, threads * 4), end="\r")
            time.sleep(30)
    except KeyboardInterrupt:
        for stop in stops:
            stop.set()
        print("Finishing current jobs.  Please wait...")
        while threading.active_count() > 1:
            time.sleep(2)
    finally:
        print("Done.")


def other():
    """Update the index and download any necessary images."""
    print("Build index (took: {}s)".format(_time(index.create)))
    print("Check disc icons (took: {}s)".format(_time(image.disc)))
    print("Check dj icons (took: {}s)".format(_time(image.icon)))
    print("Done.")


def sync():
    """Build the DJ database and front-end."""
    print("Sync dj database (took: {}s)".format(_time(database.dj)))
    print("Sync master scores (took: {}s)".format(_time(database.master)))
    print("Check dj icons (took: {}s)".format(_time(image.icon)))
    print("Build front-end (took: {}s)".format(_time(html.pages)))
    print("Done.")


def _time(function):
    """Determine the amount of time a function takes to run."""
    start_time = time.monotonic()
    function()
    return round(time.monotonic() - start_time, 2)
