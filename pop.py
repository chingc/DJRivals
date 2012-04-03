import collections
import json
import os, os.path
import re
import time
import urllib.request

import psxml


def f_clean():
    """f_clean() -> function(string)

    This function returns a function that cleans disc names.  Cleaning is done
    by stripping all non-alphanumeric characters.  The remaining characters are
    then converted to lowercase.

    """
    regex = re.compile(r"[^a-zA-Z0-9]")
    return lambda x: regex.sub(r"", x).lower()


def images():
    """images() -> None

    Download all disc images from the DJMAX site.  Files are saved in a new
    directory named "images" under the current working directory.  An image will
    be skipped if it is determined that the file already exists.  Existence is
    checked using a simple filename lookup.

    """
    # todo: make multithreaded
    url = "http://djmaxcrew.com/ranking/GetRankPopMixing.asp?p={}"
    image_url = "http://img3.djmaxcrew.com/icon/disc/110/{}"
    image_dir = "./images/"
    clean = f_clean()
    if not os.path.exists(image_dir):
        os.mkdir(image_dir)
    for page in range(1, 9):
        reply = json.loads(urllib.request.urlopen(url.format(page)).read().decode())
        for record in reply["DATA"]["RECORD"]:
            name, extension = os.path.splitext(record["DISCIMG"])
            for chart in range(1, 5):
                theirname = "{}{}{}".format(name[:-1], chart, extension)
                myname = "{}_{}{}".format(clean(record["DISCNAME"]), chart, extension)
                if os.path.exists(image_dir + myname):
                    continue
                with open(image_dir + myname, "wb") as f:
                    f.write(urllib.request.urlopen(image_url.format(theirname)).read())
                print('Wrote: "{}{}"'.format(image_dir, myname))


def index(refresh=False):
    """index([boolean]) -> dictionary

    An auto-generated dictionary with manually maintained elements.  The
    dictionary is saved as a plain text file in JSON format with the name
    "pop_index.json" under the current working directory.  This function takes
    an optional boolean value (default: False) that controls whether or not it
    should refresh its contents by checking the DJMAX site.

    Each record of the dictionary has the following structure:
    string: [string, integer, integer, integer, integer, integer]

    The key is the cleaned disc name.  The value is a list.  The first element
    is the full disc name as reported by the DJMAX site.  The remaining five
    elements are all integers.  The first four indicate the difficulty of the
    NM, HD, MX, and EX charts.  DJMAX labels these charts as 1, 2, 3, and 4,
    respectively.  The list is structured such that you can access the correct
    difficulty using DJMAX labels.  That means list index 2 returns the HD
    difficulty.  Finally, the last integer is the page number where the disc
    name shows up on the ranking page.

    Note: Because the DJMAX site does not list the difficulty level of charts
    anywhere, these entries are manually maintained.  The dictionary can be
    edited by hand in any text editor, and subsequent executions of this
    function will not clobber the manual entries.  However, if this function
    should encounter any errors while attempting to open up the JSON file, a new
    one will be generated as a replacement.  It is therefore recommended to have
    a backup of the current dictionary before using this function.

    """
    url = "http://djmaxcrew.com/ranking/GetRankPopMixing.asp?p={}"
    index_file = "./pop_index.json"
    clean = f_clean()
    try:
        with open(index_file, "rb") as f:
            index = json.loads(f.read().decode())
    except:
        index = {}
    if refresh or not index:
        for page in range(1, 9):
            reply = json.loads(urllib.request.urlopen(url.format(page)).read().decode())
            for record in reply["DATA"]["RECORD"]:
                name = record["DISCNAME"]
                if clean(name) not in index:
                    index[clean(name)] = [name, 0, 0, 0, 0, page]
                else:  # do this because the name and page could have changed
                    index[clean(name)][0] = name
                    index[clean(name)][5] = page
        output = json.dumps(index, indent=4)
        output = re.sub(r'\[\n +(".+",) +\n +(\d+,) +\n +(\d+,) +\n +(\d+,) +\n +(\d+,) +\n +(\d+)\n +\](,?) *', r'[\1 \2 \3 \4 \5 \6]\7', output)
        with open(index_file, "wb") as f:
            f.write(output.encode())
        print('Wrote: "{}"'.format(index_file))
    return index


def f_identifier():
    """f_identifier() -> function(string)

    This function returns a function that retrieves a disc identifier from the
    DJMAX site by disc name.

    """
    url = "http://djmaxcrew.com/ranking/GetRankPopMixing.asp?p={}"
    clean = f_clean()
    page = index()
    cache = {}

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
            reply = json.loads(urllib.request.urlopen(url.format(page[name][5])).read().decode())
            cache.update({clean(record["DISCNAME"]): record["DISCID"] for record in reply["DATA"]["RECORD"]})
        return cache[name]

    return identifier


def ranking(disc, chart, pages=1):
    """ranking(string, string[, integer]) -> list of tuples

    Retrieve the ranking of a specified disc name and chart.  The chart is a
    string that can be either NM, HD, MX, or EX; any other value will be treated
    as EX.  The optional integer specifies how many pages worth of rankings to
    retrieve (default: 1).  Specify 0 for a full listing.

    """
    # todo: make multithreaded
    url = "http://djmaxcrew.com/ranking/GetRankPopMixingMusic.asp?c={}&pt={}&p={}"
    identifier = f_identifier()
    disc_id = identifier(disc)
    chart = (lambda x: 1 if x == "nm" else 2 if x == "hd" else 3 if x == "mx" else 4)(chart.lower())
    results = []
    for page in range(1, 1 + (100 if pages == 0 else pages)):
        reply = json.loads(urllib.request.urlopen(url.format(disc_id, chart, page)).read().decode())
        results.extend([(record["RANK"], record["DJICON"], record["DJNAME"], record["SCORE"]) for record in reply["DATA"]["RECORD"]])
        if len(reply["DATA"]["RECORD"]) < 20:
            break
    return results


def database(disc_list=[]):
    """database([list]) -> None

    Create a local database of scores with information obtained from the DJMAX
    site.  The database is implemented as a collection of JSON files.  One JSON
    file is created for each disc.  In addition, one JSON file will be created
    for each DJ based on the information just acquired.  For the format and
    content of these files refer to data_structures.txt.  The optional argument
    is a list of strings (default: []) of cleaned disc names.  By default, it
    will create the complete database.  When given a list it will create a
    database of only those discs.  Files are saved in "./rankings/pop/disc/" and
    "./rankings/pop/dj/" under the current working directory.
    """
    # todo: write the code to generate the DJ JSON files
    start_time = time.time()
    disc_dir = "./rankings/pop/disc/"
    dj_dir = "./rankings/pop/dj/"
    if not os.path.exists(disc_dir):
        os.makedirs(disc_dir)
    if not os.path.exists(dj_dir):
        os.makedirs(dj_dir)
    disc_info = index()
    if not disc_list:
        disc_list = [title[0] for title in sorted(disc_info.items(), key=lambda i: i[1])]  # sort by page to maximize identifier() cache hits
    while len(disc_list):
        print("{} discs remaining.".format(len(disc_list)))
        disc = disc_list.pop()
        charts = ["nm", "hd", "mx", "ex"]
        output = collections.OrderedDict()
        output["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
        output["name"] = collections.OrderedDict(zip(["clean", "full"], [disc, disc_info[disc][0]]))
        output["image"] = collections.OrderedDict([(i, disc + j) for i, j in zip(["eyecatch"] + charts, [".png", "_1.png", "_2.png", "_3.png", "_4.png"])])
        output["difficulty"] = collections.OrderedDict([(i, disc_info[disc][j]) for i, j in zip(charts, [1, 2, 3, 4])])
        output["ranking"] = collections.OrderedDict()
        output["ranking"]["records"] = collections.OrderedDict()
        for chart in charts:
            try:
                results = ranking(disc, chart, 0)
                output["ranking"][chart] = results
                output["ranking"]["records"][chart] = len(results)
                print("{} {} complete.  Sleeping...".format(disc, chart))
                time.sleep(15)
            except:
                print("{} {} error.  Sleeping for 5 minutes before retrying.".format(disc, chart))
                charts.insert(0, chart)
                time.sleep(300)
        output = json.dumps(output, indent=4)
        output = re.sub(r'\[\n +(\d+,) +\n +(".*",) +\n +(".*",) +\n +(\d{6})\n +\](,?) *', r'[\1 \2 \3 \4]\5', output)
        with open(disc_dir + disc + ".json", "wb") as f:
            f.write(output.encode())
        print('Wrote: "{}{}.json"\n'.format(disc_dir, disc))
    print("Operation complete!")
    elapsed_time = round((time.time() - start_time) / 60)
    print("Database creation took {} minutes.".format(elapsed_time))


def html():
    """html() -> None

    This generates the HTML that serves as the user interface to the database.
    A required component before running this function are the difficulty levels
    for each disc and chart.  For details, see the documentation of index().
    The information is necessary because it is used to determine whether or not
    certain sections are created.  The HTML file is saved as "index.html" under
    the current working directory.
    """
    html_file = "./index.html"
    disc_info = index()
    disc_list = sorted(disc_info.keys())
    ps = psxml.PrettySimpleXML()
    ps.raw("<!DOCTYPE html>")
    ps.start("html")
    ps.start("head")
    ps.empty("meta", ['charset="UTF-8"'])
    ps.start("title", value="DJRivals", newline=False).end()
    ps.empty("link", ['rel="stylesheet"', 'type="text/css"', 'href="./css/ui-lightness/jquery-ui-1.8.18.custom.css"'])
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery-1.7.1.min.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery-ui-1.8.18.custom.min.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./djrivals.js"'], newline=False).end()
    ps.end()  # head
    ps.start("body")
    ps.start("div", attr=['class="accordion"'])
    ps.start("h3", newline=False).start("a", ['href="#"'], "Pop", newline=False).end(False).end()
    ps.start("div")
    ps.start("div", attr=['class="accordion"'])
    for chart in [(1, "NM"), (2, "HD"), (3, "MX")]:
        ps.start("h3", newline=False).start("a", ['href="#"'], chart[1], newline=False).end(False).end()
        ps.start("div")
        ps.start("div", attr=['class="pop accordion"'])
        for disc in disc_list:
            if disc_info[disc][chart[0]]:
                ps.start("h3", newline=False)
                ps.start("a", ['href="#"'], newline=False)
                ps.empty("img", ["{}{}_{}{}".format('src="./images/', disc, chart[0], '.png"')], newline=False)
                ps.raw("&nbsp " + disc_info[disc][0], newline=False)
                ps.end(False)  # a
                ps.end()  # h3
                ps.start("div")
                ps.start("p", value="Loading...", newline=False).end()
                ps.end()  # div
        ps.end()  # div
        ps.end()  # div
    ps.end_all()  # div, div, div, body, html
    with open(html_file, "wb") as f:
        f.write(ps.get().encode())
    print('Wrote: "{}"'.format(html_file))
