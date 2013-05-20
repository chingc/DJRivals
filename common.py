"""Functions common to other modules."""
import json
import os
import re
import time
import urllib.request

from settings import net


def clean(name):
    """Strip all [^a-zA-Z0-9_] characters and convert to lowercase."""
    return re.sub(r"\W", r"", name, flags=re.ASCII).lower()


def exists(path):
    """Check to see if a path exists."""
    return True if os.path.exists(path) else False


def ls(path):
    """The contents of a directory."""
    return os.listdir(path)


def mkdir(path):
    """Create the given directory path if it doesn't already exist."""
    os.makedirs(path, exist_ok=True)
    return path


def open_url(url, task):
    """Retrieve data from the specified url."""
    for attempt in range(0, net.retries):
        try:
            return urllib.request.urlopen(url)
        except OSError:
            print("Error: {} (retry in {}s)".format(task, net.wait))
            time.sleep(net.wait)
    raise ConnectionError("Halted: Unable to access resource")


def urlopen_json(url, task="Unknown task"):
    """Retrieve json data from the specified url."""
    for attempt in range(0, net.retries):
        try:
            reply = urllib.request.urlopen(url)
            reply = json.loads(reply.read().decode())
            return reply["DATA"]["RECORD"]
        except:
            print("Error: {} (retry in {}s)".format(task, net.wait))
            time.sleep(net.wait)
    raise ConnectionError("Halted: Unable to access resource")
