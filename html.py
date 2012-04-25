"""Automatic HTML generation."""
import json

from common import _dir_listing, _link, _make_dir
import psxml


def index():
    """index() -> None

    Generate the DJRivals HTML user interface based on the local database.

    """
    pop_db_dir = _make_dir(_link("pop_database_directory"))
    html_file = _link("html_file")
    charts = ["nm", "hd", "mx"]
    disc_list = sorted(_dir_listing(pop_db_dir))
    ps = psxml.PrettySimpleXML()
    ps.raw("<!DOCTYPE html>")
    ps.start("html")
    ps.start("head")
    ps.empty("meta", ['charset="UTF-8"'])
    ps.start("title", value="DJRivals", newline=False).end()
    ps.empty("link", ['rel="stylesheet"', 'type="text/css"', 'href="./css/ui-lightness/jquery-ui-1.8.19.custom.css"'])
    ps.empty("link", ['rel="stylesheet"', 'type="text/css"', 'href="./css/token-input-facebook.css"'])
    ps.empty("link", ['rel="stylesheet"', 'type="text/css"', 'href="./css/djrivals.css"'])
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery-1.7.2.min.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery-ui-1.8.19.custom.min.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery-ui-theme.switcher.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery.tablesorter.min.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery.tokeninput.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./js/djrivals.js"'], newline=False).end()
    ps.end()  # head
    ps.start("body")
    ps.start("div", ['class="accordion"'])  # start main accordion
    for chart in charts:
        ps.start("h3", newline=False).start("a", ['href="#"'], "Pop: " + chart.upper(), False).end(False).end()
        ps.start("div")  # start pop section
        ps.start("div", ['class="pop accordion"'])
        for disc in disc_list:
            with open(pop_db_dir + disc, "rb") as f:
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
    ps.start("label", ['for="myname"'], "My DJ Name", False).end()
    ps.empty("input", ['id="myname"', 'type="text"'], False).empty("br")
    ps.start("label", ['for="myrival"'], "My Rival List", False).end()
    ps.empty("input", ['id="myrival"', 'type="text"'], False).empty("br")
    ps.start("label", ['for="popcut"'], "Pop Cutoff", False).end(False).empty("br")
    ps.empty("input", ['id="popcut"', 'type="text"', 'maxlength="6"'], False).empty("br", newline=False).empty("br")
    ps.start("label", ['for="popmastercut"'], "Pop Master Cutoff", False).end(False).empty("br")
    ps.empty("input", ['id="popmastercut"', 'type="text"', 'maxlength="9"'], False).empty("br", newline=False).empty("br")
    ps.start("label", ['for="themeswitcher"'], "Theme", False).end()
    ps.start("div", ['id="themeswitcher"'], newline=False).end(False).empty("br")
    ps.start("button", ['id="save"', 'type="button"'], ":'D", False).end()
    ps.end()  # end settings section
    ps.end()  # end main accordion
    ps.end_all()  # body, html
    with open(html_file, "wb") as f:
        f.write(ps.get().encode())
    print('Wrote: "{}"'.format(html_file))
