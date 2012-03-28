import re
import time
import json
import urllib.request


def index(download=False):
    """Map each disc title to its correct page on the DJMAX site."""
    url = "http://djmaxcrew.com/ranking/GetRankPopMixing.asp?p={}"
    regex = re.compile(r"[^a-zA-Z0-9]")
    index = {
        "ad2222": 8,
        "heartbeatpart2": 7,
        "jupiterdriving": 2,
        "brandnewdays": 3,
        "melody": 2,
        "area7": 1,
        "d2": 4,
        "thelastdance": 3,
        "inmyheart": 2,
        "dreamofwinds": 5,
        "lupin": 8,
        "color": 1,
        "cyphergate": 6,
        "readynow": 6,
        "rageofdemon": 4,
        "endofthemoonlight": 1,
        "lacampanellanurave": 4,
        "getdown": 5,
        "dreamagain": 7,
        "therainmaker": 6,
        "fate": 1,
        "coloursofsorrow": 1,
        "stop": 3,
        "enemystorm": 1,
        "justfortoday": 8,
        "break": 7,
        "puzzler": 4,
        "supersonicmrfunkyremix": 4,
        "flea": 2,
        "becomemyself": 6,
        "whiteblue": 3,
        "enemystormdarkjunglemix": 6,
        "beautifulgirlsethvogtelectrovanityremix": 6,
        "eternalmemory": 3,
        "outlawreborn": 4,
        "giveme5": 7,
        "rightback": 7,
        "miles": 2,
        "coastaltempo": 1,
        "airwave": 5,
        "someday": 3,
        "lovelyhands": 5,
        "rockstar": 7,
        "rayofilluminati": 4,
        "cometome": 1,
        "toyou":1,
        "dualstrikers": 4,
        "closer": 1,
        "voyage": 3,
        "signalize": 7,
        "beyondthefuture": 5,
        "theclearbluesky": 3,
        "mister": 8,
        "desperado": 5,
        "oblivion": 2,
        "access": 1,
        "everything": 7,
        "darkprism": 7,
        "playthefuture": 3,
        "firstkiss": 2,
        "electronics": 1,
        "sweetshiningshootingstar": 3,
        "shoreline": 3,
        "lover": 2,
        "rutin": 5,
        "step": 8,
        "secretworld": 5,
        "cozyquilt": 4,
        "asktowind": 3,
        "blythe": 1,
        "cosmicfantasticlovesong": 4,
        "freedom": 2,
        "iwantyou": 2,
        "thor": 5,
        "mellowdfantasy": 6,
        "jumping": 8,
        "alifewithyou": 7,
        "lovemode": 2,
        "leavemealone": 6,
        "kungfurider": 7,
        "pianoconcertono1": 3,
        "dearmylady": 1,
        "pdm": 2,
        "honeymoon": 2,
        "keystotheworld": 2,
        "inmydream": 5,
        "bambooonbamboo": 8,
        "landscape": 2,
        "djmax": 6,
        "creator": 1,
        "jealousy": 5,
        "graveconsequence": 5,
        "proposedflowerwolfpart2": 1,
        "proposedflowerwolfpart1": 1,
        "spaceofsoul": 4,
        "youshouldgetoverme": 8,
        "yourownmiracle": 3,
        "heartofwitch": 4,
        "eternalfantasy": 5,
        "beeutiful": 4,
        "nowanewday": 7,
        "zetmrfunkyremix": 6,
        "feelmabeat": 7,
        "sweetdream": 4,
        "luvistrue": 6,
        "hexad": 2,
        "masaielectrohousemix": 6,
        "desperadonuskoolmix": 6,
        "loveisbeautiful": 5,
        "sonofsun": 3,
        "chemicalslave": 7,
        "goneastray": 6,
        "thenightstage": 5,
        "oohlala": 8,
        "beatudown": 6,
        "ai": 1,
        "seasonwarmmix": 6,
        "funkypeople": 6,
        "asktowindliveversion": 3,
        "emblem": 4,
        "luvflowfunkyhousemix": 6,
        "fermion": 2,
        "if": 6,
        "theguilty": 5,
        "burnitdown": 5,
        "cherokee": 1,
        "youme": 7,
        "trip": 4,
        "overtherainbow": 8,
        "myheartmysoul": 7,
        "hereinthemoment": 2,
        "sin": 3,
        "sayitfromyourheart": 4,
        "putemup": 4,
        "drumtown": 6,
        "blackswan": 7,
        "watchyourstep": 7,
        "fury": 2,
        "prettygirl": 8,
        "xlasher": 4,
        "monoxide": 4,
        "raisemeup": 7,
        "supersonic": 3,
        "forever": 5,
        "remember": 3,
        "novamrfunkyremix": 5,
        "hanzup": 7,
        "inthetdot": 8,
        "divineservice": 1,
        "y": 3,
        "darkenvy": 5,
        "ladymadestar": 2
    }  # pre-populate this index for faster performance
    if download:
        index.clear()
        for page in range(1, 9):
            reply = json.loads(urllib.request.urlopen(url.format(page)).read().decode())
            index.update({regex.sub(r"", record["DISCNAME"]).lower(): page for record in reply["DATA"]["RECORD"]})
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
identifier = f_identifier()


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
