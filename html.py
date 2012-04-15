"""Automatic HTML generation."""
import json

from common import _dir_listing, _link, _make_dir
import psxml


def html():
    """html() -> None

    Generate the DJRivals HTML user interface based on the local database.

    """
    pop_db_dir = _make_dir(_link("pop_database_directory"))
    html_file = _link("html_file")
    charts = ["nm", "hd", "mx"]
    ps = psxml.PrettySimpleXML()
    disc_info = []
    for disc in sorted(_dir_listing(pop_db_dir)):
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
    ps.empty("link", ['rel="stylesheet"', 'type="text/css"', 'href="./css/djrivals.css"'])
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery-1.7.1.min.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery-ui-1.8.18.custom.min.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery.tablesorter.min.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./js/djrivals.js"'], newline=False).end()
    ps.end()  # head
    ps.start("body")
    ps.start("div", ['class="accordion"'])  # start main accordion
    for chart in charts:
        ps.start("h3", newline=False).start("a", ['href="#"'], "Pop: " + chart.upper(), False).end(False).end()
        ps.start("div")  # start pop section
        ps.start("div", ['class="pop accordion"'])
        for disc in [disc for disc in disc_info if disc["records"][chart] > 0]:
            ps.start("h3", newline=False)
            ps.start("a", ['href="#"'], newline=False)
            ps.empty("img", ['src="./images/disc/{}"'.format(disc["image"][chart])], False)
            ps.raw("&nbsp " + disc["name"]["full"], newline=False)
            ps.end(False)
            ps.end()
            ps.start("div", newline=False).start("p", value="Loading...", newline=False).end(False).end()
        ps.end()
        ps.end()  # end pop section
    ps.start("h3", newline=False).start("a", ['href="#"'], "DJ Empty", False).end(False).end()
    ps.start("div", ['id="me"'])  # start me section
    ps.start("p", value="Go to settings to enter your DJ name.", newline=False).end()
    ps.end()  # end me section
    ps.start("h3", newline=False).start("a", ['href="#"'], "DJ Rivals", False).end(False).end()
    ps.start("div", ['id="rival"'])  # start rival section
    ps.start("p", value="Go to settings to enter your rivals.", newline=False).end()
    ps.end()  # end rival section
    ps.start("h3", newline=False).start("a", ['href="#"'], "Settings", False).start("span", attr=['id="status"'], newline=False).end(False).end(False).end()
    ps.start("div")  # start settings section
    ps.empty("input", ['id="myname"', 'type="text"', 'placeholder="My DJ Name"'], False).empty("br")
    ps.start("textarea", ['id="myrival"', 'cols="40"', 'rows="3"', 'placeholder="My Rival List"'], newline=False).end(False).empty("br")
    ps.start("button", ['id="save"', 'type="button"'], "YAY", False).end()
    ps.end()  # end settings section
    ps.end()  # end main accordion
    ps.end_all()  # body, html
    with open(html_file, "wb") as f:
        f.write(ps.get().encode())
    print('Wrote: "{}"'.format(html_file))


def dj():
    """dj() -> None

    Generate the HTML for the Me section for each DJ in the local database.

    """
    dj_db_dir = _make_dir(_link("dj_database_directory"))
    dj_html_dir = _make_dir(_link("dj_html_directory"))
    charts = ["nm", "hd", "mx"]
    ps = psxml.PrettySimpleXML()
    for dj in _dir_listing(dj_db_dir):
        with open(dj_db_dir + dj, "rb") as f:
            data = json.loads(f.read().decode())
        ps.start("div", ['class="accordion"'])  # start main accordion
        ps.start("h3", newline=False).start("a", ['href="#"'], "Pop", False).end(False).end()
        ps.start("div")  # start pop section
        ps.start("div", ['class="accordion"'])  # start pop accordion
        for chart in charts:
            ps.start("h3", newline=False).start("a", ['href="#"'], chart.upper(), False).end(False).end()
            ps.start("div")
            ps.start("table")
            ps.start("tr", newline=False)
            ps.start("th", value="Disc", newline=False).end(False)
            ps.start("th", value="Score", newline=False).end(False)
            ps.end()
            for score in data["pop"][chart]:
                ps.start("tr", newline=False)
                ps.start("td", value=score[0], newline=False).end(False)
                ps.start("td", value=score[1], newline=False).end(False)
                ps.end()
            ps.end()
            ps.end()
        ps.end()  # end pop accordion
        ps.end()  # end pop section
        ps.end()  # end main accordion
        with open(dj_html_dir + dj[:-5] + ".html", "wb") as f:
            f.write(ps.get().encode())
        ps.clear()
