"""Generate HTML."""
import json
import time

from common import _, _clean, _exists, _list_dir, _make_dir
from index import index
import psxml


def _head(ps):
    """Append sections that belong at the top of each page."""
    ps.beginln("head")
    ps.emptyln("meta", ['charset="UTF-8"'])
    ps.begin("title", value="DJRivals").endln()
    ps.emptyln("link", ['rel="stylesheet"', 'type="text/css"', 'href="./extern/smoothness/jquery-ui-1.9.0.custom.min.css"'])
    ps.emptyln("link", ['rel="stylesheet"', 'type="text/css"', 'href="./extern/theme-tablesorter-default.css"'])
    ps.emptyln("link", ['rel="stylesheet"', 'type="text/css"', 'href="./extern/theme-tokeninput-facebook.css"'])
    ps.emptyln("link", ['rel="stylesheet"', 'type="text/css"', 'href="./extern/djrivals.css"'])
    ps.begin("script", ['type="text/javascript"', 'src="./extern/jquery-1.8.2.min.js"']).endln()
    ps.begin("script", ['type="text/javascript"', 'src="./extern/jquery-ui-1.9.0.custom.min.js"']).endln()
    ps.begin("script", ['type="text/javascript"', 'src="./extern/jquery-tablesorter-2.4.6.min.js"']).endln()
    ps.begin("script", ['type="text/javascript"', 'src="./extern/jquery-tokeninput-1.6.0.min.js"']).endln()
    ps.begin("script", ['type="text/javascript"', 'src="./extern/djrivals.js"']).endln()
    ps.endln()  # head


def _tail(ps):
    """Append sections that belong at the bottom of each page."""
    ps.beginln("div", ['id="footer"'])
    ps.beginln("p")
    ps.begin("a", ['href="http://www.cyphergate.net/wiki/"', 'target="_blank"'], "Cypher Gate Wiki").end().rawln("&nbsp;&nbsp;")
    ps.begin("a", ['href="http://www.bemanistyle.com/forum/forumdisplay.php?7-DJMAX"', 'target="_blank"'], "DJMAX Forum (BMS)").end().rawln("&nbsp;&nbsp;")
    ps.begin("a", ['href="http://djmaxcrew.com/"', 'target="_blank"'], "DJMAX Technika").end().emptyln("br")
    ps.emptyln("br")
    ps.raw("&copy; 2012 DJ cgcgngng&#47;Cherry<br />All rights reserved.").emptyln("br")
    ps.emptyln("br")
    ps.rawln(time.strftime("%Y%m%d.%H"))
    ps.endln()  # p
    ps.endln()  # div


def _page(tabs, name, img_dir=None):
    """Generate a ranking page."""
    ps = psxml.PrettySimpleXML(2)

    ps.rawln("<!DOCTYPE html>")
    ps.beginln("html")

    _head(ps)

    ps.beginln("body")

    # jquery tabs
    ps.beginln("div", ['id="tabs"'])
    ps.beginln("ul")
    for tab in tabs:
        ps.begin("li").begin("a", ['href="#{}"'.format(tab)], tab).end().endln()
    ps.endln()  # ul
    for tab in tabs:
        ps.beginln("div", ['id="{}"'.format(tab)])
        ps.begin("p")
        if img_dir is None:
            ps.raw(name)
        else:
            ps.empty("img", ['src="./images/{}/{}_{}.png"'.format(img_dir, _clean(name), (lambda x: 2 if x == "HD" else 3 if x == "MX" else 4 if x == "EX" else 1)(tab))])
            ps.raw("&nbsp; " + name)
        ps.endln()  # p
        ps.begin("p", value="Loading...").endln()
        ps.endln()  # div
    ps.endln()  # div (tabs)

    _tail(ps)

    ps.endln()  # body
    ps.endln()  # html

    with open(_.OUTPUT_DIR + _clean(name) + ".html", "wb") as f:
        f.write(ps.output().encode())
    print('Wrote: "{}{}.html"'.format(_.OUTPUT_DIR, _clean(name)))


def _index():
    """Generate the HTML index."""
    ps = psxml.PrettySimpleXML(2)

    ps.rawln("<!DOCTYPE html>")
    ps.beginln("html")

    _head(ps)

    ps.beginln("body")

    # jquery accordion
    ps.beginln("div", ['class="accordion"'])

    ps.begin("h3", value="Rankings").endln()
    ps.beginln("div", ['id="rankings"'])
    discs = sorted(set(key for mode in (_.STAR, _.POP) for key in index(mode)))
    discsets = sorted(key for key in index(_.CLUB))
    missions = sorted(key for key in index(_.MISSION))
    ps.beginln("table")
    ps.beginln("tr")
    ps.beginln("td")
    for count, name in enumerate(discs[:]):
        ps.begin("a", ['href="./{}.html"'.format(_clean(name))], name).end().emptyln("br")
        discs.pop(0)
        if count > 107:
            break
    ps.endln()  # td
    ps.beginln("td")
    for name in discs:
        ps.begin("a", ['href="./{}.html"'.format(_clean(name))], name).end().emptyln("br")
    ps.rawln("<br /><br />")
    for name in discsets:
        ps.begin("a", ['href="./{}.html"'.format(_clean(name))], name).end().emptyln("br")
    ps.rawln("<br /><br />")
    for name in missions:
        ps.begin("a", ['href="./{}.html"'.format(_clean(name))], name).end().emptyln("br")
    ps.rawln("<br /><br />")
    ps.begin("a", ['href="./master.html"'], "Master").end().emptyln("br")
    ps.endln()  # td
    ps.endln()  # tr
    ps.endln()  # table
    ps.endln()  # div

    ps.begin("h3", value="Me").endln()
    ps.beginln("div", ['id="me"'])
    ps.begin("p", value="Go to settings to enter your DJ name.")
    ps.endln()  # p
    ps.endln()  # div

    ps.begin("h3", value="Rivals").endln()
    ps.beginln("div", ['id="rivals"'])
    ps.begin("p", value="Go to settings to enter your DJ rivals.")
    ps.endln()  # p
    ps.endln()  # div

    ps.begin("h3", value="Settings").endln()
    ps.beginln("div", ['id="settings"'])
    ps.begin("label", ['for="set_me"'], "DJ Name").end().empty("br")
    ps.empty("input", ['id="set_me"', 'type="text"']).emptyln("br")
    ps.begin("label", ['for="set_rival"'], "DJ Rivals").end().empty("br")
    ps.empty("input", ['id="set_rival"', 'type="text"']).emptyln("br")
    ps.begin("button", ['id="set_apply"', 'type="button"'], "Apply").end().raw(" ").begin("span", ['id="set_status"']).endln()
    ps.endln()  # div

    ps.begin("h3", value="About").endln()
    ps.beginln("div", ['id="about"'])
    ps.beginln("p")
    ps.rawln("DJRivals is a score tracker for DJMAX Technika 3.<br />")
    ps.emptyln("br")
    ps.rawln("Quickly and easily see your scores as well as those<br />")
    ps.rawln("from your rivals.  Score comparison shows how<br />")
    ps.rawln("far ahead or behind you are, and sortable columns<br />")
    ps.rawln("makes it simple to see your best and worst scores.<br />")
    ps.rawln("DJRivals also includes master ranking for all modes!")
    ps.endln()  # p
    ps.beginln("p", ['id="dedication"'])
    ps.rawln("Dedicated to Shoreline<br />and all Technika players.")
    ps.endln()  # p
    ps.endln()  # div

    ps.endln()  # div (accordion)

    _tail(ps)

    ps.endln()  # body
    ps.endln()  # html

    with open(_.HTML_INDEX, "wb") as f:
        f.write(ps.output().encode())
    print('Wrote: "{}"'.format(_.HTML_INDEX))


def pages():
    """Generate all ranking pages and the HTML index."""
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
            _page(tabs, name, "disc")
    for name in (key for key in index(_.CLUB)):
        if _exists(_.CLUB_DB_DIR + _clean(name) + ".json"):
            _page(["Club"], name, "club")
    for name in (key for key in index(_.MISSION)):
        if _exists(_.MISSION_DB_DIR + _clean(name) + ".json"):
            _page(["Mission"], name, "mission")
    _page(["Star", "NM", "HD", "MX", "Pop", "Club", "Mission"], "Master")
    _index()


_make_dir(_.OUTPUT_DIR)
