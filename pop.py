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
    # todo: make parallel
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
    string: [string, int, int, int, int, int]

    The key is the cleaned disc name.  The value is a list.  The first element
    is the full disc name as reported by the DJMAX site.  The remaining five
    elements are all integers.  The first four indicate the difficulty of the
    NM, HD, MX, and EX charts.  DJMAX labels these charts as 1, 2, 3, and 4,
    respectively.  The list is structured such that you can access the correct
    difficulty using DJMAX labels.  e.g. Element[2] returns the HD difficulty.
    Finally, the last integer is the page number where the disc name shows up on
    the ranking page.

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
    """Returns a function."""
    url = "http://djmaxcrew.com/ranking/GetRankPopMixing.asp?p={}"
    regex = re.compile(r"[^a-zA-Z0-9]")
    page = index()
    cache = {}

    def identifier(title):
        """Retrieve a disc identifier by disc title."""
        title = regex.sub(r"", title).lower()
        if title not in cache:
            cache.clear()
            reply = json.loads(urllib.request.urlopen(url.format(page[title])).read().decode())
            cache.update({regex.sub(r"", record["DISCNAME"]).lower(): record["DISCID"] for record in reply["DATA"]["RECORD"]})
        return cache[title]

    return identifier
#identifier = f_identifier()


def ranking(disc, chart):
    """A generator for the ranking of a specified disc title and chart."""
    url = "http://djmaxcrew.com/ranking/GetRankPopMixingMusic.asp?c={}&pt={}&p={}"
    chart = (lambda x: 1 if x == "nm" else 2 if x == "hd" else 3 if x == "mx" else 4)(chart.lower())
    for page in range(1, 50):
        reply = json.loads(urllib.request.urlopen(url.format(identifier(disc), chart, page)).read().decode())
        yield [(record["RANK"], record["DJICON"], record["DJNAME"], record["SCORE"]) for record in reply["DATA"]["RECORD"]]
        if len(reply["DATA"]["RECORD"]) < 20:
            break


def database():
    """Create a local database of scores in JSON format."""
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


def database2():
    """Create a local database of scores in XML format."""
    start_time = time.time()
    #disc_list = [title[0] for title in sorted(index().items(), key=lambda i: i[1])]  # sort by page to use cache
    disc_list = ["d2"]
    player = "<rank>{}</rank><djicon>{}</djicon><djname>{}</djname><score>{}</score>\n"
    output = """    <disc>
        <name>{}</name>
        <length>
            <normal>{}</normal>
            <hard>{}</hard>
            <maximum>{}</maximum>
            <extra>{}</extra>
        </length>
        <ranking>
            <normal>
                {}
            </normal>
            <hard>
                {}
            </hard>
            <maximum>
                {}
            </maximum>
            <extra>
                {}
            </extra>
        </ranking>
    </disc>"""
    while len(disc_list):
        disc = disc_list.pop()
        rank = []
        print("Working on '{}' ({} remaining).".format(disc, len(disc_list)))
        try:
            for chart in ["nm", "hd", "mx", "ex"]:
                results = ranking(disc, chart)
                results = [player.format(dj[0], dj[1], dj[2], dj[3]) for page in results for dj in page]
                rank.append((len(results), "".join(results)))
                print("    {} complete.  Sleeping...".format(chart))
                time.sleep(15)
            output = output.format(disc, rank[0][0], rank[1][0], rank[2][0], rank[3][0], rank[0][1], rank[1][1], rank[2][1], rank[3][1])
        except:
            print("An error occurred while working on '{}'".format(disc))
            print("Sleeping for 5 minutes before restarting.")
            disc_list.append(disc)
            time.sleep(300)
    with open("./pop.xml", "wb") as f:
        print("Writing to file.")
        f.write(output.encode())
        print("Operation complete!")
    elapsed_time = round((time.time() - start_time) / 60)
    print("Database creation took {} minutes.".format(elapsed_time))
