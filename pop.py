from collections import OrderedDict
from urllib.request import urlopen
import json
import os
import re
import time

import psxml


def _check_dir(path):
    """_check_dir(string) -> string

    Check a directory path and create it if it doesn't exist.  Returns the path
    unmodified.

    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def _f_clean():
    """_f_clean() -> function(string)

    This function returns a function that cleans disc names.  Cleaning is done
    by stripping all non-alphanumeric characters.  The remaining characters are
    then converted to lowercase.

    """
    regex = re.compile(r"[^a-zA-Z0-9]")
    return lambda x: regex.sub(r"", x).lower()


def _f_identifier():
    """_f_identifier() -> function(string)

    This function returns a function that retrieves a disc identifier from the
    DJMAX site by disc name.

    """
    # since DJMAX returns up to 20 identifiers at a time (each page lists 20
    # discs except the last page which has less than 20), the cache dictionary
    # saves these identifers to expedite future lookups.  however, since it is
    # unknown how long these identifiers stay valid, the cache size has been
    # limited to about 25% of the total number of available discs.  when the
    # cache exceeds this limit, it will clear itself and rebuild.
    def identifier(name):
        name = clean(name)
        if name not in cache:
            if len(cache) > 20:  # value of 20 means at most 40
                cache.clear()
            reply = json.loads(urlopen(url.format(page[name][5])).read().decode())
            cache.update({clean(record["DISCNAME"]): record["DISCID"] for record in reply["DATA"]["RECORD"]})
        return cache[name]

    url = "http://djmaxcrew.com/ranking/GetRankPopMixing.asp?p={}"
    clean = _f_clean()
    page = index()
    cache = {}
    return identifier


def ranking(disc, chart, pages=1):
    """ranking(string, string[, pages=integer]) -> list of tuples

    Retrieve the ranking of a specified disc name and chart.  The chart is a
    string that can be either NM, HD, MX, or EX; any other value will be treated
    as EX.  The optional integer specifies how many pages worth of rankings to
    retrieve (default: 1).  Specify 0 for a full listing.

    """
    # todo: make multithreaded
    url = "http://djmaxcrew.com/ranking/GetRankPopMixingMusic.asp?c={}&pt={}&p={}"
    identifier = _f_identifier()
    disc_id = identifier(disc)
    chart = (lambda x: 1 if x == "nm" else 2 if x == "hd" else 3 if x == "mx" else 4)(chart.lower())
    results = []
    for page in range(1, 1 + (100 if pages == 0 else pages)):
        reply = json.loads(urlopen(url.format(disc_id, chart, page)).read().decode())
        results.extend([(record["RANK"], record["DJICON"], record["DJNAME"], record["SCORE"]) for record in reply["DATA"]["RECORD"]])
        if len(reply["DATA"]["RECORD"]) < 20:
            break
    return results


def discs():
    """discs() -> None

    Download all disc images from the DJMAX site.  Files are saved under
    "./DJRivals/images/disc/".  An image will be skipped if it is determined
    that the file already exists.  Existence is checked using a simple filename
    lookup.

    """
    # todo: make multithreaded
    url = "http://djmaxcrew.com/ranking/GetRankPopMixing.asp?p={}"
    image_url = "http://img3.djmaxcrew.com/icon/disc/110/"
    image_dir = _check_dir("./DJRivals/images/disc/")
    clean = _f_clean()
    for page in range(1, 9):
        reply = json.loads(urlopen(url.format(page)).read().decode())
        for record in reply["DATA"]["RECORD"]:
            name, extension = os.path.splitext(record["DISCIMG"])
            for chart in range(1, 5):
                theirname = "{}{}{}".format(name[:-1], chart, extension)
                myname = "{}_{}{}".format(clean(record["DISCNAME"]), chart, extension)
                if os.path.exists(image_dir + myname):
                    continue
                with open(image_dir + myname, "wb") as f:
                    f.write(urlopen(image_url + theirname).read())
                print('Wrote: "{}{}"'.format(image_dir, myname))


def icons():
    """icons() -> None

    Crawl through the local database and download all necessary DJ icons from
    the DJMAX site.  Files are saved under "./DJRivals/images/icon/".  An image
    will be skipped if it is determined that the file already exists.  Existence
    is checked using a simple filename lookup.

    """
    # todo: make multithreaded
    url = "http://img3.djmaxcrew.com/icon/djicon/104/"
    pop_db_dir = _check_dir("./DJRivals/rankings/pop/disc/")
    image_dir = _check_dir("./DJRivals/images/icon/")
    icons = []
    for disc in os.listdir(pop_db_dir):
        with open(pop_db_dir + disc, "rb") as f:
            data = json.loads(f.read().decode())
        icons.extend([dj[1] for chart in ['nm', 'hd', 'mx', 'ex'] for dj in data["ranking"][chart]])
    for icon in set(icons):
        if os.path.exists(image_dir + icon):
            continue
        with open(image_dir + icon, "wb") as f:
            f.write(urlopen(url + icon).read())
        print('Wrote: "{}{}"'.format(image_dir, icon))


def index(refresh=False):
    """index([refresh=boolean]) -> dictionary

    An auto-generated dictionary with manually maintained elements.  The
    dictionary is saved in JSON format as "pop_index.json" under the current
    working directory.  An optional boolean value (default: False) controls
    whether or not it should refresh its contents by checking the DJMAX site.
    Refer to data_structures.txt for the format and contents of this file.

    Note: Because the DJMAX site does not list the difficulty level of charts,
    these entries are manually maintained.  The dictionary can be edited by hand
    in any text editor, and subsequent executions of this function will not
    clobber the manual entries.  However, if this function should encounter any
    errors while attempting to read the file, a new one will be generated as a
    replacement.  It is therefore recommended to have a backup of the current
    file before using this function.

    """
    url = "http://djmaxcrew.com/ranking/GetRankPopMixing.asp?p={}"
    index_file = "pop_index.json"
    clean = _f_clean()
    try:
        with open(index_file, "rb") as f:
            index = json.loads(f.read().decode())
    except:
        index = {}
    if refresh or not index:
        for page in range(1, 9):
            reply = json.loads(urlopen(url.format(page)).read().decode())
            for record in reply["DATA"]["RECORD"]:
                name = record["DISCNAME"]
                if clean(name) not in index:
                    index[clean(name)] = [name, 0, 0, 0, 0, page]
                else:  # do this because the name and page could have changed
                    index[clean(name)][0] = name
                    index[clean(name)][5] = page
        output = json.dumps(index, indent=4)
        output = re.sub(r'\[\n +(".+",) \n +(\d+,) \n +(\d+,) \n +(\d+,) \n +(\d+,) \n +(\d+)\n +\](,?) ?', r"[\1 \2 \3 \4 \5 \6]\7", output)
        with open(index_file, "wb") as f:
            f.write(output.encode())
        print('Wrote: "{}"'.format(index_file))
    return index


def database(disc_list=[], djs_only=False):
    """database([disc_list=list], [djs_only=boolean]) -> None

    Create a local database of scores with information obtained from the DJMAX
    site.  The database is implemented as a collection of JSON files.  One JSON
    file is created for each disc.  In addition, one JSON file will be created
    for each DJ.  The optional argument is a list of strings (default: []) of
    cleaned disc names.  By default, it will create the entire database.  Given
    a list, it will create a database of only those discs.  Files are saved
    under "./DJRivals/rankings/pop/disc/" and "./DJRivals/rankings/pop/dj/".
    Refer to data_structures.txt for the format and contents of these files.

    """
    def _rankings():
        """This portion creates the ranking database."""
        while len(disc_list):
            print("{} discs remaining.".format(len(disc_list)))
            disc = disc_list.pop()
            charts = ["nm", "hd", "mx", "ex"]
            output = OrderedDict()
            output["name"] = OrderedDict([("clean", disc), ("full", disc_info[disc][0])])
            output["image"] = OrderedDict([(i, disc + j) for i, j in zip(["eyecatch"] + charts, [".png", "_1.png", "_2.png", "_3.png", "_4.png"])])
            output["difficulty"] = OrderedDict([(i, disc_info[disc][j]) for i, j in zip(charts, [1, 2, 3, 4])])
            output["ranking"] = OrderedDict()
            output["ranking"]["records"] = OrderedDict()
            for chart in charts:
                try:
                    results = ranking(disc, chart, 0)
                    output["ranking"][chart] = results
                    output["ranking"]["records"][chart] = len(results)
                    print("{} {} complete.  Sleeping...".format(disc, chart))
                    time.sleep(10)
                except:
                    print("{} {} error.  Sleeping for 5 minutes before retrying.".format(disc, chart))
                    charts.insert(0, chart)
                    time.sleep(300)
            output = json.dumps(output, indent=4)
            output = re.sub(r'\[\n +(\d+,) \n +(".*",) \n +(".*",) \n +(\d{6})\n +\](,?) ?', r"[\1 \2 \3 \4]\5", output)
            with open("{}{}.json".format(disc_dir, disc), "wb") as f:
                f.write(output.encode())
            print('Wrote: "{}{}.json"\n'.format(disc_dir, disc))

    def _djs():
        """This portion creates the DJ database."""
        djs = {}
        print("Writing DJ files...\n")
        for json_file in sorted(os.listdir(disc_dir)):
            with open(disc_dir + json_file, "rb") as f:
                data = json.loads(f.read().decode())
            for chart in ["nm", "hd", "mx", "ex"]:
                for dj in data["ranking"][chart]:
                    disc = data["name"]["clean"]
                    name = dj[2]
                    score = dj[3]
                    if name.find("*") > -1: name = name.replace("*", "(8)")
                    if name.find("/") > -1: name = name.replace("/", "(fs)")
                    if name.find("?") > -1: name = name.replace("?", "(qm)")
                    if name.find(":") > -1: name = name.replace(":", "(;)")
                    if name.lower().startswith("con"): name = "(-)" + name   # i never knew this
                    if name not in djs:
                        djs[name] = OrderedDict()
                    if disc not in djs[name]:
                        djs[name][disc] = OrderedDict()
                    djs[name][disc][chart] = score
        for k, v in djs.items():
            with open("./DJRivals/rankings/pop/dj/{}.json".format(k), "wb") as f:
                f.write(json.dumps(v, indent=4).encode())

    start_time = time.time()
    disc_dir = _check_dir("./DJRivals/rankings/pop/disc/")
    dj_dir = _check_dir("./DJRivals/rankings/pop/dj/")
    disc_info = index()
    if not djs_only:
        if not disc_list:
            disc_list = [disc[0] for disc in sorted(disc_info.items(), key=lambda x: x[1][5])]  # sort by page to maximize identifier() cache hits
        _rankings()
    _djs()
    elapsed_time = round((time.time() - start_time) / 60)
    print("Finished!\n\nDatabase creation took {} minutes.".format(elapsed_time))


def html():
    """html() -> None

    Crawl through the local database and automatically generate the DJRivals
    HTML user interface.  The HTML file is saved as "./DJRivals/index.html".

    """
    pop_db_dir = _check_dir("./DJRivals/rankings/pop/disc/")
    html_file = "./DJRivals/index.html"
    charts = ["nm", "hd", "mx", "ex"]
    ps = psxml.PrettySimpleXML()
    disc_info = []
    for disc in sorted(os.listdir(pop_db_dir)):
        with open(pop_db_dir + disc, "rb") as f:
            data = json.loads(f.read().decode())
        extracted = {}
        extracted["name"] = data["name"]
        extracted["image"] = data["image"]
        extracted["level"] = data["difficulty"]
        extracted["records"] = data["ranking"]["records"]
        disc_info.append(extracted)
    ps.raw("<!DOCTYPE html>")
    ps.start("html")
    ps.start("head")
    ps.empty("meta", ['charset="UTF-8"'])
    ps.start("title", value="DJRivals", newline=False).end()
    ps.empty("link", ['rel="stylesheet"', 'type="text/css"', 'href="./css/ui-lightness/jquery-ui-1.8.18.custom.css"'])
    ps.empty("link", ['rel="stylesheet"', 'type="text/css"', 'href="./djrivals.css"'])
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery-1.7.1.min.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery-ui-1.8.18.custom.min.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./djrivals.js"'], newline=False).end()
    ps.end()  # head
    ps.start("body")
    ps.start("div", attr=['class="accordion"'])
    ps.start("h3", newline=False).start("a", ['href="#"'], "Pop", newline=False).end(False).end()
    ps.start("div")
    ps.start("div", attr=['class="accordion"'])
    for chart in charts:
        ps.start("h3", newline=False).start("a", ['href="#"'], chart.upper(), newline=False).end(False).end()
        ps.start("div")
        ps.start("div", attr=['class="pop accordion"'])
        for disc in [disc for disc in disc_info if disc["records"][chart] > 0]:
            ps.start("h3", newline=False)
            ps.start("a", ['href="#"'], newline=False)
            ps.empty("img", ['src="./images/disc/{}"'.format(disc["image"][chart])], newline=False)
            ps.raw("&nbsp " + disc["name"]["full"], newline=False)
            ps.end(False)  # a
            ps.end()  # h3
            ps.start("div", newline=False).start("p", value="Loading...", newline=False).end(False).end()
        ps.end()  # div
        ps.end()  # div
    ps.end_all()  # div, div, div, body, html
    with open(html_file, "wb") as f:
        f.write(ps.get().encode())
    print('Wrote: "{}"'.format(html_file))
