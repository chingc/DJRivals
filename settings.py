"""Directory and program settings."""

class _Namespace():
    """Namespace for various settings."""
    pass


### Output Directories ###

path = _Namespace()
path.root = "../smwst.github.io/DJRivals/"

path.db = _Namespace()
path.db.root    = path.root + "database/"
path.db.dj      = path.db.root + "dj/"
path.db.star    = path.db.root + "star/"
path.db.nm      = path.db.root + "nm/"
path.db.hd      = path.db.root + "hd/"
path.db.mx      = path.db.root + "mx/"
path.db.ex      = path.db.root + "ex/"
path.db.club    = path.db.root + "club/"
path.db.mission = path.db.root + "mission/"
path.db.master  = path.db.root + "master/"

path.index = _Namespace()
path.index.root = path.db.root
path.index.db   = path.index.root + "db_index.json"
path.index.dj   = path.index.root + "dj_index.json"

path.img = _Namespace()
path.img.root    = path.root + "images/"
path.img.icon    = path.img.root + "icon/"
path.img.star    = path.img.root + "disc/"
path.img.pop     = path.img.star
path.img.club    = path.img.root + "club/"
path.img.mission = path.img.root + "mission/"


### Program Settings ###

net = _Namespace()
net.retries = 5
net.wait    = 180  # seconds


### DJMAX website and game settings -- DO NOT CHANGE ###

url = _Namespace()
url.ranking = _Namespace()
url.ranking.base    = "http://djmaxcrew.com/ranking/"
url.ranking.star    = url.ranking.base + "GetRankStarMixingMusic.asp?c={}&p={}"
url.ranking.pop     = url.ranking.base + "GetRankPopMixingMusic.asp?c={}&p={}"
url.ranking.club    = url.ranking.base + "GetRankClubMixingMusic.asp?c={}&p={}"
url.ranking.mission = url.ranking.base + "GetRankMissionDetail.asp?mp={}&p={}"

url.id = _Namespace()
url.id.base    = url.ranking.base
url.id.star    = url.id.base + "GetRankStarMixing.asp?p={}"
url.id.pop     = url.id.base + "GetRankPopMixing.asp?p={}"
url.id.club    = url.id.base + "GetRankClubMixing.asp?p={}"
url.id.mission = url.id.base + "GetRankMission.asp"

url.img = _Namespace()
url.img.base    = "http://img3.djmaxcrew.com/icon/"
url.img.icon    = url.img.base + "djicon/104/{}"
url.img.star    = url.img.base + "disc/110/{}"
url.img.pop     = url.img.star
url.img.club    = url.img.base + "discset/134/{}"
url.img.mission = url.img.base + "missionpack/{}"

site = _Namespace()
site.key = _Namespace()
site.key.star    = {"name": "DISCNAME", "id": "DISCID", "image": "DISCIMG"}
site.key.pop     = site.key.star
site.key.club    = {"name": "DISCSETNAME", "id": "DISCSETID", "image": "DISCSETIMG"}
site.key.mission = {"name": "MISSIONPACKNAME", "id": "MISSIONPACKID", "image": "MISSIONPACKICON"}

site.pages = _Namespace()
site.pages.star    = 9
site.pages.pop     = 9
site.pages.club    = 1
site.pages.mission = 1

game = _Namespace()
game.mode = _Namespace()
game.mode.star    = "star"
game.mode.pop     = "pop"
game.mode.club    = "club"
game.mode.mission = "mission"

game.chart = _Namespace()
game.chart.nm = {"str": "nm", "int": 1}
game.chart.hd = {"str": "hd", "int": 2}
game.chart.mx = {"str": "mx", "int": 3}
game.chart.ex = {"str": "ex", "int": 4}
