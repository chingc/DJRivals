"""DJRivals database updater."""
from time import localtime, sleep, strftime, time

import dj
import html
import image
import master
import pop


def database():
    """database() -> None

    Continuous incremental updates of the database.

    """
    try:
        while(True):
            disc_list = pop.index()
            disc_list = sorted(disc_list.keys(), key=lambda x: disc_list[x]["timestamp"])
            interval = int(24 * 60 * 60 / len(disc_list))
            for disc in disc_list:
                pop.database([disc])
                print("\nNext incremental update at: " + strftime("%H:%M:%S", localtime(time() + interval)))
                print("Ctrl-C to quit.\n")
                sleep(interval)
    except KeyboardInterrupt:
        print("Please wait...")
        dj.database()
        master.database()
        image.icons()
        print("Done.")


def index():
    """index() -> None

    Update the index file, generate the html for DJRivals, and retrieve new disc
    images if any.

    """
    pop.index(True)
    html.index()
    image.discs()
