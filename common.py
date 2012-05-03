"""Variables and functions common to other modules."""
import os
import re


class _Constant():
    """Namespace for constants."""
    pass


def _clean(name):
    """Strip all [^a-zA-Z0-9_] characters and convert to lowercase."""
    return re.sub(r"\W", r"", name, flags=re.ASCII).lower()


def _exists(path):
    """Check to see if a path exists."""
    return True if os.path.exists(path) else False


def _list_dir(path):
    """The contents of a directory."""
    return os.listdir(path)


def _make_dir(path):
    """Create the given directory path if it doesn't already exist."""
    if not os.path.exists(path):
        os.makedirs(path)
    return path


_ = _Constant()

_.STAR    = 0
_.POP     = 1
_.CLUB    = 2
_.MISSION = 3

_.CHARTS = ["nm", "hd", "mx"]

_.STAR_ID_URL      = "http://djmaxcrew.com/ranking/GetRankStarMixing.asp?p={}"
_.STAR_RANKING_URL = "http://djmaxcrew.com/ranking/GetRankStarMixingMusic.asp?c={}&p={}"

_.POP_ID_URL      = "http://djmaxcrew.com/ranking/GetRankPopMixing.asp?p={}"
_.POP_RANKING_URL = "http://djmaxcrew.com/ranking/GetRankPopMixingMusic.asp?c={}&p={}"

_.CLUB_ID_URL      = "http://djmaxcrew.com/ranking/GetRankClubMixing.asp?p={}"
_.CLUB_RANKING_URL = "http://djmaxcrew.com/ranking/GetRankClubMixingMusic.asp?c={}&p={}"

_.MISSION_ID_URL      = "http://djmaxcrew.com/ranking/GetRankMission.asp"
_.MISSION_RANKING_URL = "http://djmaxcrew.com/ranking/GetRankMissionDetail.asp?mp={}&p={}"

_.DJ_DB_DIR      = "./DJRivals/database/dj/"
_.STAR_DB_DIR    = "./DJRivals/database/star/"
_.POP_DB_DIR     = "./DJRivals/database/pop/"
_.CLUB_DB_DIR    = "./DJRivals/database/club/"
_.MISSION_DB_DIR = "./DJRivals/database/mission/"
_.MASTER_DB_DIR  = "./DJRivals/database/master/"

_.DJ_INDEX      = "./DJRivals/database/dj_index.json"
_.STAR_INDEX    = "./DJRivals/database/star_index.json"
_.POP_INDEX     = "./DJRivals/database/pop_index.json"
_.CLUB_INDEX    = "./DJRivals/database/club_index.json"
_.MISSION_INDEX = "./DJRivals/database/mission_index.json"
_.HTML_INDEX    = "./DJRivals/index.html"

_.ICON_IMAGE_URL    = "http://img3.djmaxcrew.com/icon/djicon/104/{}"
_.DISC_IMAGE_URL    = "http://img3.djmaxcrew.com/icon/disc/110/{}"
_.CLUB_IMAGE_URL    = "http://img3.djmaxcrew.com/icon/discset/134/{}"
_.MISSION_IMAGE_URL = "http://img3.djmaxcrew.com/icon/missionpack/{}"

_.ICON_IMAGE_DIR    = "./DJRivals/images/icon/"
_.DISC_IMAGE_DIR    = "./DJRivals/images/disc/"
_.CLUB_IMAGE_DIR    = "./DJRivals/images/club/"
_.MISSION_IMAGE_DIR = "./DJRivals/images/mission/"
