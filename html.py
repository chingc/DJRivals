"""Automatic HTML generation."""
from common import _dir_listing, _link, _make_dir

import psxml


def html():
    """html() -> None

    Generate the DJRivals HTML user interface based on database contents.

    """
    pop_db_dir = _make_dir(_link("pop_database_directory"))
    html_file = _link("html_file")
    charts = ["nm", "hd", "mx", "ex"]
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
    ps.empty("link", ['rel="stylesheet"', 'type="text/css"', 'href="./djrivals.css"'])
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery-1.7.1.min.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./js/jquery-ui-1.8.18.custom.min.js"'], newline=False).end()
    ps.start("script", ['type="text/javascript"', 'src="./djrivals.js"'], newline=False).end()
    ps.end()  # head
    ps.start("body")
    ps.start("div", attr=['class="accordion"'])  # start main accordion
    ps.start("h3", newline=False).start("a", ['href="#"'], "Pop", newline=False).end(False).end()
    ps.start("div")  # start pop section
    ps.start("div", attr=['class="accordion"'])
    for chart in charts:
        ps.start("h3", newline=False).start("a", ['href="#"'], chart.upper(), newline=False).end(False).end()
        ps.start("div")
        ps.start("div", attr=['class="pop accordion"'])
        for disc in [disc for disc in disc_info if disc["records"][chart] > 0]:
            ps.start("h3", newline=False)
            ps.start("a", ['href="#"'], newline=False)
            ps.empty("img", ['src="./images/disc/{}"'.format(disc["image"][chart])], newline=False)
            ps.raw("&nbsp " + disc["name"]["full"], newline=False)
            ps.end(False)
            ps.end()
            ps.start("div", newline=False).start("p", value="Loading...", newline=False).end(False).end()
        ps.end()
        ps.end()
    ps.end()
    ps.end()  # end pop section
    ps.start("h3", newline=False).start("a", ['href="#"'], "Me", newline=False).end(False).end()
    ps.start("div")  # start me section
    ps.start("div", attr=['class="me accordion"'])
    for score in ["299950 PP++", "299900 PP+", "299800 PP", "297", "295", "290", "285", "280", "270", "< 270", "No Play"]:
        ps.start("h3", newline=False).start("a", ['href="#"'], score, newline=False).end(False).end()
        ps.start("div", newline=False).start("p", value="Loading...", newline=False).end(False).end()
    ps.end()
    ps.end()  # end me section
    ps.start("h3", newline=False).start("a", ['href="#"'], "Rival", newline=False).end(False).end()
    ps.start("div")  # start rival section
    ps.start("div", attr=['class="rival accordion"'])
    for rival in ["Rival A", "Rival B", "Rival C"]:
        ps.start("h3", newline=False).start("a", ['href="#"'], rival, newline=False).end(False).end()
        ps.start("div", newline=False).start("p", value="Loading...", newline=False).end(False).end()
    ps.end()
    ps.end()  # end rival section
    ps.end()  # end main accordion
    ps.end_all()  # body, html
    with open(html_file, "wb") as f:
        f.write(ps.get().encode())
    print('Wrote: "{}"'.format(html_file))
