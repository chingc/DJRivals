"""DJRival directory and program settings."""

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
path.index.root    = path.db.root
path.index.dj      = path.index.root + "dj_index.json"
path.index.star    = path.index.root + "star_index.json"
path.index.pop     = path.index.root + "pop_index.json"
path.index.club    = path.index.root + "club_index.json"
path.index.mission = path.index.root + "mission_index.json"

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
site.key.disc    = {"name": "DISCNAME", "id": "DISCID", "image": "DISCIMG"}
site.key.club    = {"name": "DISCSETNAME", "id": "DISCSETID", "image": "DISCSETIMG"}
site.key.mission = {"name": "MISSIONPACKNAME", "id": "MISSIONPACKID", "image": "MISSIONPACKICON"}

site.pages = _Namespace()
site.pages.star    = 9
site.pages.pop     = 9
site.pages.club    = 1
site.pages.mission = 1

mode = _Namespace()
mode.star    = "Star"
mode.pop     = "Pop"
mode.club    = "Club"
mode.mission = "Mission"

chart = _Namespace()
chart.nm = {"str": "NM", "int": 1}
chart.hd = {"str": "HD", "int": 2}
chart.mx = {"str": "MX", "int": 3}
chart.ex = {"str": "EX", "int": 4}

net = _Namespace()
net.retries = 10
net.wait    = 180
