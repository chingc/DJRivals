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

_.RANKING_URL = "http://djmaxcrew.com/ranking/"
_.ICON_URL    = "http://img3.djmaxcrew.com/icon/"
_.OUTPUT_DIR  = "../smwst.github.com/DJRivals/"

_.STAR_ID_URL    = _.RANKING_URL + "GetRankStarMixing.asp?p={}"
_.POP_ID_URL     = _.RANKING_URL + "GetRankPopMixing.asp?p={}"
_.CLUB_ID_URL    = _.RANKING_URL + "GetRankClubMixing.asp?p={}"
_.MISSION_ID_URL = _.RANKING_URL + "GetRankMission.asp"

_.STAR_RANKING_URL    = _.RANKING_URL + "GetRankStarMixingMusic.asp?c={}&p={}"
_.POP_RANKING_URL     = _.RANKING_URL + "GetRankPopMixingMusic.asp?c={}&p={}"
_.CLUB_RANKING_URL    = _.RANKING_URL + "GetRankClubMixingMusic.asp?c={}&p={}"
_.MISSION_RANKING_URL = _.RANKING_URL + "GetRankMissionDetail.asp?mp={}&p={}"

_.ICON_IMAGE_URL    = _.ICON_URL + "djicon/104/{}"
_.DISC_IMAGE_URL    = _.ICON_URL + "disc/110/{}"
_.CLUB_IMAGE_URL    = _.ICON_URL + "discset/134/{}"
_.MISSION_IMAGE_URL = _.ICON_URL + "missionpack/{}"

_.DJ_DB_DIR      = _.OUTPUT_DIR + "database/dj/"
_.STAR_DB_DIR    = _.OUTPUT_DIR + "database/star/"
_.POP_DB_DIR     = _.OUTPUT_DIR + "database/pop/"
_.CLUB_DB_DIR    = _.OUTPUT_DIR + "database/club/"
_.MISSION_DB_DIR = _.OUTPUT_DIR + "database/mission/"
_.MASTER_DB_DIR  = _.OUTPUT_DIR + "database/master/"

_.DJ_INDEX      = _.OUTPUT_DIR + "database/dj_index.json"
_.STAR_INDEX    = _.OUTPUT_DIR + "database/star_index.json"
_.POP_INDEX     = _.OUTPUT_DIR + "database/pop_index.json"
_.CLUB_INDEX    = _.OUTPUT_DIR + "database/club_index.json"
_.MISSION_INDEX = _.OUTPUT_DIR + "database/mission_index.json"
_.HTML_INDEX    = _.OUTPUT_DIR + "index.html"

_.ICON_IMAGE_DIR    = _.OUTPUT_DIR + "images/icon/"
_.DISC_IMAGE_DIR    = _.OUTPUT_DIR + "images/disc/"
_.CLUB_IMAGE_DIR    = _.OUTPUT_DIR + "images/club/"
_.MISSION_IMAGE_DIR = _.OUTPUT_DIR + "images/mission/"
