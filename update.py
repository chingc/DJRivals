"""DJRivals database updater."""
from time import localtime, sleep, strftime, time

from common import _
import database
import image
import index


def indexes():
    """Update indexes, retrieve new images if any, and generate the html."""
    index.touch(_.STAR, True)
    index.touch(_.POP, True)
    index.touch(_.CLUB, True)
    index.touch(_.MISSION, True)
    image.mode(_.STAR)
    image.mode(_.POP)
    image.mode(_.CLUB)
    image.mode(_.MISSION)
    index.html()


def mode(mode):
    """Continuous incremental updates of the specified database."""
    if mode == _.STAR:
        data  = index.touch(_.STAR)
        hours = 12
    elif mode == _.POP:
        data  = index.touch(_.POP)
        hours = 20
    elif mode == _.CLUB:
        data  = index.touch(_.CLUB)
        hours = 8
    elif mode == _.MISSION:
        data  = index.touch(_.MISSION)
        hours = 8
    else:
        raise ValueError("invalid argument")
    try:
        while(True):
            names = sorted(data.keys(), key=lambda x: data[x]["timestamp"])
            interval = (hours * 60 * 60 / len(names))
            while names:
                database.build(mode, names.pop(0))
                print("\n{} items remaining in this update cycle.".format(len(names)))
                print("Next incremental update at: {} (Ctrl-C to Quit)\n".format(strftime("%H:%M:%S", localtime(time() + interval))))
                sleep(interval)
    except KeyboardInterrupt:
        print("Done.")


def finish():
    """Build non-game mode databases."""
    database.dj()
    database.master()
    image.icon()
    print("Done.")
