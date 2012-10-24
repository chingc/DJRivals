"""Generate HTML."""
import json
import time

from common import _, _clean, _exists, _list_dir, _make_dir
from index import index
import psxml


def _page(name, tabs):
    """Write doc."""
    ps = psxml.PrettySimpleXML(2)

    # doctype, html
    ps.rawln("<!DOCTYPE html>")
    ps.beginln("html")

    # head
    ps.beginln("head")
    ps.emptyln("meta", ['charset="UTF-8"'])
    ps.begin("title", value="DJRivals").endln()

    # stylesheet
    ps.emptyln("link", ['rel="stylesheet"', 'type="text/css"', 'href="../extern/smoothness/jquery-ui-1.9.0.custom.min.css"'])
    ps.emptyln("link", ['rel="stylesheet"', 'type="text/css"', 'href="../extern/djrivals.css"'])

    # javascript
    ps.begin("script", ['type="text/javascript"', 'src="../extern/jquery-1.8.2.js"']).endln()
    ps.begin("script", ['type="text/javascript"', 'src="../extern/jquery-ui-1.9.0.custom.min.js"']).endln()
    ps.begin("script", ['type="text/javascript"', 'src="../extern/djrivals.js"']).endln()

    # head
    ps.endln()

    # body
    ps.beginln("body")

    # jquery tabs
    ps.beginln("div", ['id="tabs"'])
    ps.beginln("ul")
    for tab in tabs:
        ps.begin("li").begin("a", ['href="#{}"'.format(tab)], tab).end().endln()
    ps.endln()
    for tab in tabs:
        ps.beginln("div", ['id="{}"'.format(tab)])
        ps.begin("p")
        ps.empty("img", ['src="../images/disc/{}_{}.png"'.format(_clean(name), (lambda x: 2 if x == "HD" else 3 if x == "MX" else 4 if x == "EX" else 1)(tab))])
        ps.raw(name)
        ps.endln()
        ps.begin("p", value="Loading...").endln()
        ps.endln()
    ps.endln()

    # copyright
    ps.beginln("div", ['id="copyright"'])
    ps.begin("p", value="DJRivals copyright (c), DJ cgcgngng<br />All rights reserved.").endln()
    ps.begin("p", value="Images copyright (c), NEOWIZ and PENTAVISION<br />All rights reserved.").endln()
    ps.endln()

    # body, html
    ps.endln()
    ps.endln()

    with open(_.HTML_PAGES + _clean(name) + ".html", "wb") as f:
        f.write(ps.output().encode())
    print('Wrote: "{}{}.html"'.format(_.HTML_PAGES, _clean(name)))


def pages():
    """Doc."""
    for name in set(key for mode in (_.STAR, _.POP) for key in index(mode)):
        tabs = []
        clean_name = _clean(name)
        if _exists(_.STAR_DB_DIR + clean_name + ".json"):
            tabs.append("Star")
        if _exists(_.POP_NM_DB_DIR + clean_name + ".json"):
            tabs.append("NM")
        if _exists(_.POP_HD_DB_DIR + clean_name + ".json"):
            tabs.append("HD")
        if _exists(_.POP_MX_DB_DIR + clean_name + ".json"):
            tabs.append("MX")
        if _exists(_.POP_EX_DB_DIR + clean_name + ".json"):
            tabs.append("EX")
        if len(tabs) > 0:
            _page(name, tabs[:])


def html():
    # TODO: rewrite
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


_make_dir(_.HTML_PAGES)
