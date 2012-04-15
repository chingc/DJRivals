"""Pop database creation."""
from collections import OrderedDict
from urllib.request import urlopen
import json
import time

from common import _clean, _dir_listing, _file_exists, _link, _make_dir


def _f_identifier():
    """Retrieves a disc identifier from the DJMAX site by disc name."""
    def identifier(disc):
        # DJMAX returns up to 20 identifiers at a time (each page lists 20 discs
        # except the last page which has less than 20), so this function uses a
        # cache to expedite future lookups.  however, since it is unknown how
        # long these identifiers stay valid, the cache size has been limited to
        # about 25% of the total number of available discs.  when the cache
        # exceeds this limit, it will clear itself and rebuild.
        if disc not in cache:
            if len(cache) > 20:  # value of 20 means at most 40
                cache.clear()
            data = json.loads(urlopen(url.format(info[disc]["page"])).read().decode())["DATA"]["RECORD"]
            cache.update({record["DISCNAME"]: record["DISCID"] for record in data})
        return cache[disc]

    url = _link("pop_ranking_page_url")
    info = index()
    cache = {}
    return identifier


def _ranking(disc_id, chart):
    """The complete ranking of the specified disc identifier and chart."""
    # todo: make multithreaded
    url = _link("pop_ranking_disc_url")
    chart = (lambda x: 1 if x == "nm" else 2 if x == "hd" else 3 if x == "mx" else 4)(chart)
    results = []
    for page in range(1, 100):
        data = json.loads(urlopen(url.format(disc_id, chart, page)).read().decode())["DATA"]["RECORD"]
        results.extend([(record["RANK"], record["DJICON"], record["DJNAME"], record["SCORE"]) for record in data])
        if len(data) < 20:
            break
    return results


def index(refresh=False):
    """index([refresh=boolean]) -> dictionary

    An auto-generated dictionary with manually maintained elements.  An optional
    boolean value (default: False) controls whether or not it should refresh its
    contents by checking the DJMAX site.  Refer to data_structures.txt for the
    format and contents of this file.

    Note: Because the DJMAX site does not list the difficulty level of charts,
    these entries are manually maintained.  The dictionary can be edited by hand
    in any text editor, and subsequent executions of this function will not
    clobber the manual entries.  However, if this function should encounter any
    errors while attempting to read the file, a new one will be generated as a
    replacement.  It is therefore recommended to have a backup of the current
    file before using this function.

    """
    url = _link("pop_ranking_page_url")
    index_file = _link("index_file")
    try:
        with open(index_file, "rb") as f:
            index = json.loads(f.read().decode(), object_pairs_hook=OrderedDict)
    except:
        index = {}
    if refresh or not index:
        for page in range(1, 9):
            data = json.loads(urlopen(url.format(page)).read().decode())["DATA"]["RECORD"]
            for record in data:
                disc = record["DISCNAME"]
                if disc not in index:
                    index[disc] = OrderedDict([("page", 0), ("nm", 0), ("hd", 0), ("mx", 0), ("ex", 0)])
                index[disc]["page"] = page
        with open(index_file, "wb") as f:
            f.write(json.dumps(OrderedDict(sorted(index.items())), indent=4).encode())
        print('Wrote: "{}"'.format(index_file))
    return index


def database(disc_list=[]):
    """database([disc_list=list]) -> None

    Create a local database of scores with information obtained from the DJMAX
    site.  The database is implemented as a collection of JSON files.  One JSON
    file is created for each disc.  The optional argument is a list of strings
    (default: []) of clean disc names.  The entire database is created by
    default, but incremental updates can be performed by utilizing the optional
    argument.  Refer to data_structures.txt for the format and contents of these
    files.

    """
    start_time = time.time()
    pop_db_dir = _make_dir(_link("pop_database_directory"))
    identifier = _f_identifier()
    info = index()
    if not disc_list:
        disc_list = [disc for disc in sorted(info.keys(), key=lambda x: info[x]["page"])]  # sort by page to maximize identifier() cache hits
    while len(disc_list):
        print("{} discs remaining.".format(len(disc_list)))
        disc = disc_list.pop()
        clean_disc = _clean(disc)
        charts = ["nm", "hd", "mx"]
        output = OrderedDict()
        output["timestamp"] = int(time.time())
        output["name"] = disc
        output["eyecatch"] = clean_disc + ".png"
        for chart in charts:
            output[chart] = OrderedDict()
            output[chart]["icon"] = "{}_{}.png".format(clean_disc, 1 if chart == "nm" else 2 if chart == "hd" else 3 if chart == "mx" else 4)
            output[chart]["difficulty"] = info[disc][chart]
            try:
                results = _ranking(identifier(disc), chart)
                output[chart]["records"] = len(results)
                output[chart]["ranking"] = results
                print("{} {} complete.  Sleeping...".format(clean_disc, chart))
                time.sleep(10)
            except:
                print("{} {} error.  Sleeping for 5 minutes before retrying.".format(clean_disc, chart))
                charts.insert(0, chart)
                time.sleep(300)
        with open("{}{}.json".format(pop_db_dir, clean_disc), "wb") as f:
            f.write(json.dumps(output).encode())
        print('Wrote: "{}{}.json"\n'.format(pop_db_dir, clean_disc))
    elapsed_time = round((time.time() - start_time) / 60)
    print("Database creation took {} minutes.".format(elapsed_time))
