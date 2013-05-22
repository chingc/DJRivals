"""Generate HTML."""
import json
import time

from common import clean, exists
from settings import game, path
import index
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


def _tail(sm, idx=None):
    """Append sections that belong at the bottom of each page."""
    sm.beginln("div", [("id", "footer")])
    sm.beginln("p")
    sm.begin("a", [("href", "http://www.cyphergate.net/wiki/"), ("target", "_blank")], "Cypher Gate Wiki").end().rawln("&nbsp;&nbsp;")
    sm.begin("a", [("href", "http://www.bemanistyle.com/forum/forumdisplay.php?7-DJMAX"), ("target", "_blank")], "DJMAX Forum (BMS)").end().rawln("&nbsp;&nbsp;")
    sm.begin("a", [("href", "http://djmaxcrew.com/"), ("target", "_blank")], "DJMAX Technika").end().emptyln("br")
    sm.emptyln("br")
    sm.rawln("&copy; 2012 DJ cgcgngng&#47;Cherry<br />All rights reserved.")
    if idx:
        sm.rawln("<br /><br />")
        avg_age = [0, 0]
        for mode in (game.mode.star, game.mode.pop, game.mode.club, game.mode.mission):
            avg_age[0] += len(idx[mode])
            avg_age[1] += sum(idx[mode][key]["timestamp"] for key in idx[mode])
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
            sm.empty("img", [("src", "{}/{}_{}.png".format(img_dir, clean(name), (lambda x: 2 if x == "HD" else 3 if x == "MX" else 4 if x == "EX" else 1)(tab)))])
            sm.raw("&nbsp; " + name)
        sm.endln()  # p
        sm.begin("p", value="Loading...").endln()
        sm.endln()  # div
    sm.endln()  # div (tabs)

    _tail(sm)

    sm.endln()  # body
    sm.endln()  # html

    with open(path.root + clean(name) + ".html", "wb") as f:
        f.write(sm.output().encode())
    #print('Wrote: "{}{}.html"'.format(path.root, clean(name)))


def _index(idx):
    """Generate the HTML index."""
    discs = sorted(set(key for mode in (game.mode.star, game.mode.pop) for key in idx[mode]))
    discsets = sorted(key for key in idx[game.mode.club])
    missions = sorted(key for key in idx[game.mode.mission])

    sm = simplemarkup.SimpleMarkup(2)

    sm.rawln("<!DOCTYPE html>")
    sm.beginln("html")

    _head(sm)

    sm.beginln("body")

    # jquery accordion
    sm.beginln("div", [("id", "root")])

    sm.begin("h3", value="Rankings").endln()
    sm.beginln("div", [("id", "rankings")])
    sm.beginln("table")
    sm.beginln("tr")
    sm.beginln("td")
    for count, name in enumerate(discs[:]):
        sm.begin("a", [("href", "./{}.html".format(clean(name)))], name).end().emptyln("br")
        discs.pop(0)
        if count > 107:  # no more than this number of items in the first column
            break
    sm.endln()  # td
    sm.beginln("td")  # here starts the second column
    for name in discs:
        sm.begin("a", [("href", "./{}.html".format(clean(name)))], name).end().emptyln("br")
    sm.rawln("<br /><br />")
    for name in discsets:
        sm.begin("a", [("href", "./{}.html".format(clean(name)))], name).end().emptyln("br")
    sm.rawln("<br /><br />")
    for name in missions:
        sm.begin("a", [("href", "./{}.html".format(clean(name)))], name).end().emptyln("br")
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

    _tail(sm, idx)

    sm.endln()  # body
    sm.endln()  # html

    with open(path.root + "index.html", "wb") as f:
        f.write(sm.output().encode())
    #print('Wrote: "{}index.html"'.format(path.root))


def pages():
    """Generate all ranking pages and the HTML index."""
    def get_str(chart):
        return chart["str"].upper()

    def mk_cap(mode):
        return mode.capitalize()

    idx = index.read()
    for name in set(key for mode in (game.mode.star, game.mode.pop) for key in idx[mode]):
        tabs = []
        clean_name = clean(name)
        if exists(path.db.star + clean_name + ".json"): tabs.append(mk_cap(game.mode.star))
        if exists(path.db.nm + clean_name + ".json"): tabs.append(get_str(game.chart.nm))
        if exists(path.db.hd + clean_name + ".json"): tabs.append(get_str(game.chart.hd))
        if exists(path.db.mx + clean_name + ".json"): tabs.append(get_str(game.chart.mx))
        if exists(path.db.ex + clean_name + ".json"): tabs.append(get_str(game.chart.ex))
        if len(tabs) > 0:
            _page(tabs, name, "./images/disc")
    for name in (key for key in idx[game.mode.club]):
        if exists(path.db.club + clean(name) + ".json"):
            _page([mk_cap(game.mode.club)], name, "./images/club")
    for name in (key for key in idx[game.mode.mission]):
        if exists(path.db.mission + clean(name) + ".json"):
            _page([mk_cap(game.mode.mission)], name, "./images/mission")
    _page([mk_cap(game.mode.star), get_str(game.chart.nm), get_str(game.chart.hd), get_str(game.chart.mx), mk_cap(game.mode.pop), mk_cap(game.mode.club), mk_cap(game.mode.mission)], "Master")
    _index(idx)
