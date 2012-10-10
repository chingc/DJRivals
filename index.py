"""Index management."""
from collections import OrderedDict
from urllib.request import urlopen
import json
import time

from common import _, _clean, _exists, _list_dir, _make_dir
import psxml


def touch(mode, refresh=False, reset=False):
    """Create, update, or retrieve an index.

    Any of the four integer constants defined in the common module can be given
    as an argument.  It will create, update, or retrieve an index of that type.
    The first boolean value (default: False) controls whether or not to perform
    an index refresh by checking the DJMAX site.  The second boolean, when set
    to True, will reset the timestamp to zero (default: False).  The timestamps
    track when a particular database has been updated.

    Note: The Star and Pop indexes contain elements that need to be manually
    maintained because the DJMAX site does not list the difficulty level of
    charts.  They can be edited by hand in any text editor, and subsequent
    executions of this function will not clobber these entries.

    """
    if mode == _.STAR:
        url     = _.STAR_ID_URL
        ifile   = _.STAR_INDEX
        db_dir  = _make_dir(_.STAR_DB_DIR)
        stop    = _.STAR_PAGES
        key     = _.DISC_KEY["name"]
        members = [("timestamp", 0), ("page", 0), ("level", 0)]
    elif mode == _.POP:
        url     = _.POP_ID_URL
        ifile   = _.POP_INDEX
        db_dir  = _make_dir(_.POP_DB_DIR)
        stop    = _.POP_PAGES
        key     = _.DISC_KEY["name"]
        members = [("timestamp", 0), ("page", 0), ("nm", 0), ("hd", 0), ("mx", 0), ("ex", 0)]
    elif mode == _.CLUB:
        url     = _.CLUB_ID_URL
        ifile   = _.CLUB_INDEX
        db_dir  = _make_dir(_.CLUB_DB_DIR)
        stop    = _.CLUB_PAGES
        key     = _.CLUB_KEY["name"]
        members = [("timestamp", 0), ("page", 0)]
    elif mode == _.MISSION:
        url     = _.MISSION_ID_URL
        ifile   = _.MISSION_INDEX
        db_dir  = _make_dir(_.MISSION_DB_DIR)
        stop    = _.MISSION_PAGES
        key     = _.MISSION_KEY["name"]
        members = [("timestamp", 0), ("page", 0)]
    else:
        raise ValueError("invalid argument")
    if _exists(ifile):
        with open(ifile, "rb") as f:
            index = json.loads(f.read().decode(), object_pairs_hook=OrderedDict)
    else:
        index = {}
    if refresh or not index:
        for page in range(1, stop + 1):
            data = json.loads(urlopen(url.format(page)).read().decode())["DATA"]["RECORD"]
            for record in data:
                name = record[key]
                if name not in index:
                    index[name] = OrderedDict(members)
                if reset:
                    index[name]["timestamp"] = 0
                index[name]["page"] = page
        with open(ifile, "wb") as f:
            f.write(json.dumps(OrderedDict(sorted(index.items())), indent=2).encode())
        print('Wrote: "{}"'.format(ifile))
    return index


def html():
    """Generate the DJRivals HTML index file."""
    star_db_dir    = _make_dir(_.STAR_DB_DIR)
    pop_db_dir     = _make_dir(_.POP_DB_DIR)
    club_db_dir    = _make_dir(_.CLUB_DB_DIR)
    mission_db_dir = _make_dir(_.MISSION_DB_DIR)

    star_list    = sorted(_list_dir(star_db_dir))
    pop_list     = sorted(_list_dir(pop_db_dir))
    club_list    = sorted(_list_dir(club_db_dir))
    mission_list = sorted(_list_dir(mission_db_dir))

    ps = psxml.PrettySimpleXML()

    # doctype, html
    ps.raw("<!DOCTYPE html>")
    ps.start("html")

    # head
    ps.start("head")
    ps.empty("meta", ['charset="UTF-8"'])
    ps.start("title", value="DJRivals", newline=False).end()

    # stylesheet
    for stylesheet in ["ui-lightness/jquery-ui-1.8.20.custom.css", "token-input-facebook.css", "tablesorter-blue.css", "djrivals.css"]:
        ps.empty("link", ['rel="stylesheet"', 'type="text/css"', 'href="./css/{}"'.format(stylesheet)])

    # javascript
    for javascript in ["jquery-1.7.2.min.js", "jquery-ui-1.8.20.custom.min.js", "jquery-ui-theme.switcher.js", "jquery.tablesorter.min.js", "jquery.tokeninput.js", "djrivals.js"]:
        ps.start("script", ['type="text/javascript"', 'src="./js/{}"'.format(javascript)], newline=False).end()

    # head
    ps.end()

    # body, root accordion
    ps.start("body")
    ps.start("div", ['id="root"', 'class="accordion"'])

    # star
    ps.start("h3", newline=False).start("a", ['href="#"'], "Star", False).end(False).end()
    ps.start("div")
    ps.start("div", ['id="star"', 'class="accordion"'])
    for name in star_list:
        with open(star_db_dir + name, "rb") as f:
            data = json.loads(f.read().decode())
        if data["records"] > 0:
            ps.start("h3", newline=False)
            ps.start("a", ['href="#"'], newline=False)
            ps.empty("img", ['src="./images/disc/{}"'.format(data["icon"])], False)
            ps.raw("&nbsp " + data["name"], newline=False)
            ps.end(False)
            ps.end()
            ps.start("div", newline=False).start("p", value="Loading...", newline=False).end(False).end()
    ps.end()
    ps.end()

    # pop
    for chart in _.CHARTS:
        ps.start("h3", newline=False).start("a", ['href="#"'], "Pop: " + chart.upper(), False).end(False).end()
        ps.start("div")
        ps.start("div", ['class="pop accordion"'])
        for name in pop_list:
            with open(pop_db_dir + name, "rb") as f:
                data = json.loads(f.read().decode())
            if data[chart]["records"] > 0:
                ps.start("h3", newline=False)
                ps.start("a", ['href="#"'], newline=False)
                ps.empty("img", ['src="./images/disc/{}"'.format(data[chart]["icon"])], False)
                ps.raw("&nbsp " + data["name"], newline=False)
                ps.end(False)
                ps.end()
                ps.start("div", newline=False).start("p", value="Loading...", newline=False).end(False).end()
        ps.end()
        ps.end()

    # club
    ps.start("h3", newline=False).start("a", ['href="#"'], "Club", False).end(False).end()
    ps.start("div")
    ps.start("div", ['id="club"', 'class="accordion"'])
    for name in club_list:
        with open(club_db_dir + name, "rb") as f:
            data = json.loads(f.read().decode())
        if data["records"] > 0:
            ps.start("h3", newline=False)
            ps.start("a", ['href="#"'], newline=False)
            ps.empty("img", ['src="./images/club/{}"'.format(data["icon"])], False)
            ps.raw("&nbsp " + data["name"], newline=False)
            ps.end(False)
            ps.end()
            ps.start("div", newline=False).start("p", value="Loading...", newline=False).end(False).end()
    ps.end()
    ps.end()

    # mission
    ps.start("h3", newline=False).start("a", ['href="#"'], "Mission", False).end(False).end()
    ps.start("div")
    ps.start("div", ['id="mission"', 'class="accordion"'])
    for name in mission_list:
        with open(mission_db_dir + name, "rb") as f:
            data = json.loads(f.read().decode())
        if data["records"] > 0:
            ps.start("h3", newline=False)
            ps.start("a", ['href="#"'], newline=False)
            ps.empty("img", ['src="./images/mission/{}"'.format(data["icon"])], False)
            ps.raw("&nbsp " + data["name"], newline=False)
            ps.end(False)
            ps.end()
            ps.start("div", newline=False).start("p", value="Loading...", newline=False).end(False).end()
    ps.end()
    ps.end()
    ps.empty("br", newline=False).empty("br")

    # master ranking
    for master in ["Star Master", "Pop Master", "Club Master", "Mission Master"]:
        ps.start("h3", newline=False).start("a", ['href="#"'], master, False).end(False).end()
        ps.start("div", ['id="{}"'.format(_clean(master))])
        ps.start("p", value="Loading...", newline=False).end()
        ps.end()
    ps.empty("br", newline=False).empty("br")

    # personal/rival
    for string in [("DJ Empty", "me", "Go to settings to enter your DJ name."), ("DJ Rivals", "rival", "Go to settings to enter your rivals.")]:
        ps.start("h3", newline=False).start("a", ['href="#"'], string[0], False).end(False).end()
        ps.start("div", ['id="{}"'.format(string[1])])
        ps.start("p", value=string[2], newline=False).end()
        ps.end()
    ps.empty("br", newline=False).empty("br")

    # settings
    ps.start("h3", newline=False).start("a", ['href="#"'], "Settings", False).end(False).end()
    ps.start("div")
    ps.start("label", ['for="myname"'], "My DJ Name", False).end()
    ps.empty("input", ['id="myname"', 'type="text"'], False).empty("br")
    ps.start("label", ['for="myrival"'], "My Rival List", False).end()
    ps.empty("input", ['id="myrival"', 'type="text"'], False).empty("br")
    ps.start("table", ['id="cutoff"'])
    for cutoff in [("Star Cutoff", "Star Master Cutoff", 6, 8), ("Pop Cutoff", "Pop Master Cutoff", 6, 9), ("Club Cutoff", "Club Master Cutoff", 7, 8), ("Mission Cutoff", "Mission Master Cutoff", 7, 8)]:
        clean = _clean(cutoff[0])
        ps.start("tr")
        ps.start("td")
        ps.start("label", ['for="{}"'.format(clean)], cutoff[0], False).end(False).empty("br")
        ps.empty("input", ['id="{}"'.format(clean), 'type="text"', 'maxlength="{}"'.format(cutoff[2])], False).empty("br", newline=False).empty("br")
        ps.end()
        clean = _clean(cutoff[1])
        ps.start("td")
        ps.start("label", ['for="{}"'.format(clean)], cutoff[1], False).end(False).empty("br")
        ps.empty("input", ['id="{}"'.format(clean), 'type="text"', 'maxlength="{}"'.format(cutoff[3])], False).empty("br", newline=False).empty("br")
        ps.end()
        ps.end()
    ps.end()
    ps.start("label", ['for="themeswitcher"'], "Theme", False).end()
    ps.start("div", ['id="themeswitcher"'], newline=False).end(False).empty("br")
    ps.start("button", ['id="save"', 'type="button"'], ":'D", False).end(False).raw(" ", False).start("span", attr=['id="status"'], newline=False).end()
    ps.end()

    # about
    ps.start("h3", newline=False).start("a", ['href="#"'], "About", False).end(False).end()
    ps.start("div")
    ps.start("div", ['id="about"'])
    ps.raw("DJRivals is a score tracker for DJMAX Technika 3.")
    ps.empty("br", newline=False).empty("br")
    ps.raw("Track personal scores, track the scores of your rivals,", False).empty("br")
    ps.raw("and even see score comparisons.  Sortable columns", False).empty("br")
    ps.raw("makes it easy to see your best and worst scores.")
    ps.empty("br", newline=False).empty("br")
    ps.raw("Star Master, Club Master, and Mission Master", False).empty("br")
    ps.raw("rankings available nowhere else!")
    ps.end()
    ps.start("div", ['id="dedication"'])
    ps.raw("Dedicated to Shoreline", False).empty("br")
    ps.raw("and all Technika players.")
    ps.empty("hr")
    ps.start("a", ['href="http://www.cyphergate.net/wiki/"', 'target="_blank"'], "Cypher Gate Wiki", False).end(False).empty("br")
    ps.start("a", ['href="http://www.bemanistyle.com/forum/forumdisplay.php?7-DJMAX"', 'target="_blank"'], "DJMAX Forum (BMS)", False).end(False).empty("br")
    ps.start("a", ['href="http://djmaxcrew.com/"', 'target="_blank"'], "DJMAX Technika", False).end()
    ps.end()
    ps.end()

    # root accordion
    ps.end()

    # copyright
    ps.start("div", ['id="copyright"'])
    ps.raw("DJRivals copyright (c), DJ cgcgngng", False).empty("br")
    ps.raw("All rights reserved.")
    ps.empty("br", newline=False).empty("br")
    ps.raw("Images copyright (c), NEOWIZ and PENTAVISION", False).empty("br")
    ps.raw("All rights reserved.")
    ps.empty("br", newline=False).empty("br")
    ps.raw("Updated: " + time.strftime("%Y%m%d"))
    ps.end()

    # body, html
    ps.end_all()

    with open(_.HTML_INDEX, "wb") as f:
        f.write(ps.get().encode())
    print('Wrote: "{}"'.format(_.HTML_INDEX))
