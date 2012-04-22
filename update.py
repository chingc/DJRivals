"""DJRivals database updater."""
from time import localtime, sleep, strftime, time

import pop
import dj
import image
import html


def pop():
    """pop() -> None

    Continuous incremental updates of the pop database.

    """
    while(True):
        print("Beginning new cycle...\n")
        disc_list = pop.index()
        disc_list = sorted(disc_list.keys(), key=lambda x: disc_list[x]["timestamp"])
        interval = int(24 * 60 * 60 / len(disc_list))
        for disc in disc_list:
            pop.database([disc])
            print("\nNext incremental update at: " + strftime("%H:%M:%S", localtime(time() + interval)))
            print("Ctrl-C to quit.\n")
            sleep(interval)
        print("\nFull database update complete.\n")


def djs():
    """djs() -> None

    Update the DJ database and retrieve any necessary icons.

    """
    dj.database()
    image.icons()


def index():
    """index() -> None

    Update the index file, generate the html for DJRivals, and retrieve new disc
    images if available.

    """
    pop.index(True)
    html.index()
    image.discs()
