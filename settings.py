"""DJRivals directory and program settings."""

class _Namespace():
    """Namespace for various settings."""
    pass


path = _Namespace()
path.root = "../djr_test/"

path.db = _Namespace()
path.db.root    = path.root + "database/"
path.db.dj      = path.db.root + "dj/"
path.db.star    = path.db.root + "star/"
path.db.nm      = path.db.root + "pop_nm/"
path.db.hd      = path.db.root + "pop_hd/"
path.db.mx      = path.db.root + "pop_mx/"
path.db.ex      = path.db.root + "pop_ex/"
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
path.img.disc    = path.img.root + "disc/"
path.img.club    = path.img.root + "club/"
path.img.mission = path.img.root + "mission/"

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
url.img.disc    = url.img.base + "disc/110/{}"
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
game.mode.star    = "Star"
game.mode.pop     = "Pop"
game.mode.club    = "Club"
game.mode.mission = "Mission"

game.chart = _Namespace()
game.chart.nm  = {"str": "NM", "int": 1}
game.chart.hd  = {"str": "HD", "int": 2}
game.chart.mx  = {"str": "MX", "int": 3}
game.chart.ex  = {"str": "EX", "int": 4}

net = _Namespace()
net.retries = 10
net.wait    = 180
