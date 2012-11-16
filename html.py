"""Generate HTML."""
import json
import time

from common import _, _clean, _exists, _list_dir, _make_dir
from index import index
import simplemarkup


def _head(sm):
    """Append sections that belong at the top of each page."""
    sm.beginln("head")
    sm.emptyln("meta", [("charset", "UTF-8")])
    sm.begin("title", value="DJRivals").endln()
    sm.emptyln("link", [("rel", "stylesheet"), ("type", "text/css"), ("href", "./extern/smoothness/jquery-ui-1.9.1.min.css")])
    sm.emptyln("link", [("rel", "stylesheet"), ("type", "text/css"), ("href", "./extern/theme-tablesorter-default.css")])
    sm.emptyln("link", [("rel", "stylesheet"), ("type", "text/css"), ("href", "./extern/theme-tokeninput-facebook.css")])
    sm.emptyln("link", [("rel", "stylesheet"), ("type", "text/css"), ("href", "./extern/djrivals.css")])
    sm.begin("script", [("type", "text/javascript"), ("src", "./extern/jquery-1.8.2.min.js")]).endln()
    sm.begin("script", [("type", "text/javascript"), ("src", "./extern/jquery-ui-1.9.1.min.js")]).endln()
    sm.begin("script", [("type", "text/javascript"), ("src", "./extern/jquery-tablesorter-2.2.2.min.js")]).endln()
    sm.begin("script", [("type", "text/javascript"), ("src", "./extern/jquery-tokeninput-1.6.0.min.js")]).endln()
    sm.begin("script", [("type", "text/javascript"), ("src", "./extern/djrivals.min.js")]).endln()
    sm.endln()  # head


def _tail(sm, print_time):
    """Append sections that belong at the bottom of each page."""
    sm.beginln("div", [("id", "footer")])
    sm.beginln("p")
    sm.begin("a", [("href", "http://www.cyphergate.net/wiki/"), ("target", "_blank")], "Cypher Gate Wiki").end().rawln("&nbsp;&nbsp;")
    sm.begin("a", [("href", "http://www.bemanistyle.com/forum/forumdisplay.php?7-DJMAX"), ("target", "_blank")], "DJMAX Forum (BMS)").end().rawln("&nbsp;&nbsp;")
    sm.begin("a", [("href", "http://djmaxcrew.com/"), ("target", "_blank")], "DJMAX Technika").end().emptyln("br")
    sm.emptyln("br")
    sm.rawln("&copy; 2012 DJ cgcgngng&#47;Cherry<br />All rights reserved.")
    if print_time:
        sm.rawln("<br /><br />")
        avg_age = [0, 0]
        for index in (_.STAR_INDEX, _.POP_INDEX, _.CLUB_INDEX, _.MISSION_INDEX):
            with open(index, "rb") as f:
                data = json.loads(f.read().decode())
            avg_age[0] += len(data)
            avg_age[1] += sum(data[name]["timestamp"] for name in data)
        avg_age = avg_age[1] / avg_age[0]
        sm.rawln(time.strftime("%Y%m%d.%H", time.localtime(avg_age)))
    sm.endln()  # p
    sm.endln()  # div


def _page(tabs, name, img_dir=None):
    """Generate a ranking page."""
    sm = simplemarkup.SimpleMarkup(2)

    sm.rawln("<!DOCTYPE html>")
    sm.beginln("html")

    _head(sm)

    sm.beginln("body")

    # jquery tabs
    sm.beginln("div", [("id", "ranking")])
    sm.beginln("ul")
    for tab in tabs:
        sm.begin("li").begin("a", [("href", "#" + tab)], tab).end().endln()
    sm.endln()  # ul
    for tab in tabs:
        sm.beginln("div", [("id", tab)])
        sm.begin("p")
        if img_dir is None:
            sm.raw(name)
        else:
            sm.empty("img", [("src", "./images/{}/{}_{}.png".format(img_dir, _clean(name), (lambda x: 2 if x == "HD" else 3 if x == "MX" else 4 if x == "EX" else 1)(tab)))])
            sm.raw("&nbsp; " + name)
        sm.endln()  # p
        sm.begin("p", value="Loading...").endln()
        sm.endln()  # div
    sm.endln()  # div (tabs)

    _tail(sm, False)

    sm.endln()  # body
    sm.endln()  # html

    with open(_.HTML_DIR + _clean(name) + ".html", "wb") as f:
        f.write(sm.output().encode())
    print('Wrote: "{}{}.html"'.format(_.HTML_DIR, _clean(name)))


def _index():
    """Generate the HTML index."""
    sm = simplemarkup.SimpleMarkup(2)

    sm.rawln("<!DOCTYPE html>")
    sm.beginln("html")

    _head(sm)

    sm.beginln("body")

    # jquery accordion
    sm.beginln("div", [("id", "root")])

    sm.begin("h3", value="Rankings").endln()
    sm.beginln("div", [("id", "rankings")])
    discs = sorted(set(key for mode in (_.STAR, _.POP) for key in index(mode)))
    discsets = sorted(key for key in index(_.CLUB))
    missions = sorted(key for key in index(_.MISSION))
    sm.beginln("table")
    sm.beginln("tr")
    sm.beginln("td")
    for count, name in enumerate(discs[:]):
        sm.begin("a", [("href", "./{}.html".format(_clean(name)))], name).end().emptyln("br")
        discs.pop(0)
        if count > 107:
            break
    sm.endln()  # td
    sm.beginln("td")
    for name in discs:
        sm.begin("a", [("href", "./{}.html".format(_clean(name)))], name).end().emptyln("br")
    sm.rawln("<br /><br />")
    for name in discsets:
        sm.begin("a", [("href", "./{}.html".format(_clean(name)))], name).end().emptyln("br")
    sm.rawln("<br /><br />")
    for name in missions:
        sm.begin("a", [("href", "./{}.html".format(_clean(name)))], name).end().emptyln("br")
    sm.rawln("<br /><br />")
    sm.begin("a", [("href", "./master.html")], "Master").end().emptyln("br")
    sm.endln()  # td
    sm.endln()  # tr
    sm.endln()  # table
    sm.endln()  # div

    sm.begin("h3", value="Me").endln()
    sm.beginln("div", [("id", "me")])
    sm.begin("p", value="Go to settings to enter your DJ name.")
    sm.endln()  # p
    sm.endln()  # div

    sm.begin("h3", value="Rivals").endln()
    sm.beginln("div", [("id", "rivals")])
    sm.begin("p", value="Go to settings to enter your DJ rivals.")
    sm.endln()  # p
    sm.endln()  # div

    sm.begin("h3", value="Settings").endln()
    sm.beginln("div", [("id", "settings")])
    sm.begin("label", [("for", "set_me")], "DJ Name").end().empty("br")
    sm.empty("input", [("id", "set_me"), ("type", "text")]).emptyln("br")
    sm.begin("label", [("for", "set_rival")], "DJ Rivals").end().empty("br")
    sm.empty("input", [("id", "set_rival"), ("type", "text")]).emptyln("br")
    sm.begin("button", [("id", "set_apply"), ("type", "button")], "Apply").end().raw(" ").begin("span", [("id", "set_status")]).endln()
    sm.endln()  # div

    sm.begin("h3", value="About").endln()
    sm.beginln("div", [("id", "about")])
    sm.beginln("p")
    sm.rawln("DJRivals is a score tracker for DJMAX Technika 3.<br />")
    sm.emptyln("br")
    sm.rawln("Quickly and easily see your scores as well as those<br />")
    sm.rawln("from your rivals.  Score comparison shows how<br />")
    sm.rawln("far ahead or behind you are, and sortable columns<br />")
    sm.rawln("makes it simple to see your best and worst scores.<br />")
    sm.rawln("DJRivals also includes master ranking for all modes!")
    sm.endln()  # p
    sm.beginln("p", [("id", "dedication")])
    sm.rawln("Dedicated to Shoreline<br />and all Technika players.")
    sm.endln()  # p
    sm.endln()  # div

    sm.endln()  # div (accordion)

    _tail(sm, True)

    sm.endln()  # body
    sm.endln()  # html

    with open(_.HTML_DIR + "index.html", "wb") as f:
        f.write(sm.output().encode())
    print('Wrote: "{}index.html"'.format(_.HTML_DIR))


def pages():
    """Generate all ranking pages and the HTML index."""
    for name in set(key for mode in (_.STAR, _.POP) for key in index(mode)):
        tabs = []
        clean_name = _clean(name)
        if _exists(_.STAR_DB_DIR + clean_name + ".json"):
            tabs.append(_.STAR)
        if _exists(_.POP_NM_DB_DIR + clean_name + ".json"):
            tabs.append(_.NM)
        if _exists(_.POP_HD_DB_DIR + clean_name + ".json"):
            tabs.append(_.HD)
        if _exists(_.POP_MX_DB_DIR + clean_name + ".json"):
            tabs.append(_.MX)
        if _exists(_.POP_EX_DB_DIR + clean_name + ".json"):
            tabs.append(_.EX)
        if len(tabs) > 0:
            _page(tabs, name, "disc")
    for name in (key for key in index(_.CLUB)):
        if _exists(_.CLUB_DB_DIR + _clean(name) + ".json"):
            _page([_.CLUB], name, "club")
    for name in (key for key in index(_.MISSION)):
        if _exists(_.MISSION_DB_DIR + _clean(name) + ".json"):
            _page([_.MISSION], name, "mission")
    _page([_.STAR, _.NM, _.HD, _.MX, _.POP, _.CLUB, _.MISSION], "Master")
    _index()


_make_dir(_.HTML_DIR)
