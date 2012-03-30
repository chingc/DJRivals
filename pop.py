import json
import os, os.path
import re
import time
import urllib.request


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
    should refresh its contents by going to the DJMAX site.

    Each record of the dictionary has the following structure:
    string: [string, integer, integer, integer, integer, integer]

    The key is the cleaned disc name.  The value is a list.  The first element
    is the full disc name as reported by the DJMAX site.  The remaining five
    elements are all integers.  The first four indicate the difficulty of the
    NM, HD, MX, and EX charts.  DJMAX labels these charts as 1, 2, 3, and 4,
    respectively.  The list is structured such that you can access the correct
    difficulty using DJMAX labels.  e.g. Element[2] returns the HD difficulty.
    Finally, the last integer is the page number where the disc name shows up on
    the ranking page.

    Note: Because the DJMAX site does not list the difficulty level of charts
    anywhere, these entries are manually maintained.  The dictionary can be
    edited by hand in any text editor, and subsequent executions of this
    function will not clobber the manual entries.  However, if this function
    encounters any errors while attempting to open up the dictionary a new one
    will be generated as a replacement.  It is therefore recommended to have a
    backup of the current dictionary before running a refresh.

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
        output = re.sub(r', ?\n *(\d)', r', \1', output)  # condense records to one line
        output = re.sub(r'\n *\](,?) ?', r']\1', output)  # adjust closing braceket
        output = re.sub(r'\[ ?\n *"', r'["', output)  # adjust opening bracket
        with open(index_file, "wb") as f:
            f.write(output.encode())
        print('Index written to: "{}"'.format(index_file))
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
    """ranking(string, string[, integer]) -> list

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


def database_json():
    """Create a local database of scores in JSON format."""
    # todo: fix; currently broken
    start_time = time.time()
    disc_list = [title[0] for title in sorted(index().items(), key=lambda i: i[1])]  # sort by page to use cache
    ranking_key = ("rank", "djicon", "djname", "score")
    output = {}
    while len(disc_list):
        disc = disc_list.pop()
        output[disc] = {}
        output[disc]["length"] = {}
        output[disc]["ranking"] = {}
        print("Working on '{}' ({} remaining).".format(disc, len(disc_list)))
        try:
            for chart in ["nm", "hd", "mx"]:
                results = ranking(disc, chart)
                results = [dict(zip(ranking_key, dj)) for page in results for dj in page]
                output[disc]["length"][chart] = len(results)
                output[disc]["ranking"][chart] = results
                print("    {} complete.  Sleeping...".format(chart))
                time.sleep(15)
        except:
            print("An error occurred while working on '{}'".format(disc))
            print("Sleeping for 5 minutes before restarting.")
            disc_list.append(disc)
            time.sleep(300)
    print("Cleaning output.")
    output = json.dumps(output, indent=4)
    output = re.sub(r'(["\d],) \n +"', r'\1 "', output)  # condense scores to one line
    output = re.sub(r'([^\]\}])\n +}', r'\1 }', output)  # adjust closing brace
    output = re.sub(r'([,\[] ?\n +\{)\n +"', r'\1 "', output)  # adjust opening brace
    with open("./pop.json", "wb") as f:
        print("Writing to file.")
        f.write(output.encode())
        print("Operation complete!")
    elapsed_time = round((time.time() - start_time) / 60)
    print("Database creation took {} minutes.".format(elapsed_time))


def database_xml():
    """Create a local database of scores in XML format."""
    # todo: clean up
    # todo: documentation
    def psxml():    # i didn't want to create a class, so i made this closure
        """Pretty Simple XML: A simple little pretty print XML generator."""
        o = []      # open tags
        x = ""      # xml output string
        n = True    # newline
        i = "    "  # indent width
        d = 0       # depth of current level
        def prefix():
            return d * i if n else ""
        def suffix(newline):
            nonlocal n
            n = newline
            return "\n" if newline else ""
        def psopen(tag, newline=True):
            nonlocal x, d
            x += "{}<{}>{}".format(prefix(), tag, suffix(newline))
            d += 1
            o.append(tag)
        def psclose(newline=True):
            nonlocal x, d
            d -= 1
            x += "{}</{}>{}".format(prefix(), o.pop(), suffix(newline))
        def pstag(tag, value, newline=True):
            nonlocal x
            x += "{}<{}>{}</{}>{}".format(prefix(), tag, value, tag, suffix(newline))
        def psget():
            return x
        return (psopen, psclose, pstag, psget)

    start_time = time.time()
    psopen, psclose, pstag, psget = psxml()
    disc_info = index()
    #disc_list = [title[0] for title in sorted(index().items(), key=lambda i: i[1])]  # sort by page to use cache
    disc_list = ["theclearbluesky"]

    psopen("root")
    while len(disc_list):
        records = {}
        disc = disc_list.pop()
        print("Working on '{}' ({} remaining).".format(disc, len(disc_list)))
        charts = ["nm", "hd", "mx", "ex"]
        for chart in charts:
            try:
                records[chart] = ranking(disc, chart, 0)
                print("    {} complete.  Sleeping...".format(chart))
                time.sleep(15)
            except:
                print("An error occurred while working on '{} {}'".format(disc, chart))
                print("Sleeping for 5 minutes before restarting.")
                charts.insert(0, chart)
                time.sleep(300)
        psopen("disc")
        psopen("name")
        pstag("clean", disc)
        pstag("full", disc_info[disc][0])
        psclose()  # name
        psopen("image")
        pstag("eyecatch", disc + ".png")
        pstag("nm", disc + "_1.png")
        pstag("hd", disc + "_2.png")
        pstag("mx", disc + "_3.png")
        pstag("ex", disc + "_4.png")
        psclose()  # image
        psopen("difficulty")
        pstag("nm", disc_info[disc][1])
        pstag("hd", disc_info[disc][2])
        pstag("mx", disc_info[disc][3])
        pstag("ex", disc_info[disc][4])
        psclose()  # difficulty
        psopen("ranking")
        psopen("length")
        for chart in ["nm", "hd", "mx", "ex"]:
            pstag(chart, len(records[chart]))
        psclose()  # length
        for chart in ["nm", "hd", "mx", "ex"]:
            psopen(chart)
            for dj in records[chart]:
                psopen("dj", False)
                pstag("rank", dj[0], False)
                pstag("icon", dj[1], False)
                pstag("name", dj[2], False)
                pstag("score", dj[3], False)
                psclose()  # dj
            psclose()  # chart
        psclose()  # ranking
        psclose()  # disc
    psclose()  # root
    with open("./pop_ranking.xml", "wb") as f:
        print("Writing to file.")
        f.write(psget().encode())
        print("Operation complete!")
    elapsed_time = round((time.time() - start_time) / 60)
    print("Database creation took {} minutes.".format(elapsed_time))
