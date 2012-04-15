"""DJRivals database updater."""
from random import shuffle
from time import localtime, sleep, strftime, time

import pop
import dj
import image
import html


def continuous():
    """continuous() -> None

    Continuous incremental updates of the DJRivals database.

    """
    while(True):
        print("Beginning new cycle...\n")
        disc_list = list(pop.index().keys())
        interval = int(24 * 60 * 60 / len(disc_list))
        shuffle(disc_list)
        for disc in disc_list:
            pop.database([disc])
            print("\nNext incremental update at: " + strftime("%H:%M:%S", localtime(time() + interval)))
            print("Ctrl-C to quit.\n")
            sleep(interval)
        dj.database()
        image.icons()
        html.html()
        print("Full database update complete.\n")


def index():
    """index() -> None

    Update the index file and retrieve new disc images if available.

    """
    pop.index(True)
    image.discs()
