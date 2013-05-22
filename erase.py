"""Initializer."""
import shutil

from common import mkdir
from settings import path


def initialize():
    shutil.rmtree(path.root)
    mkdir(path.root)
    mkdir(path.db.root)
    mkdir(path.db.dj)
    mkdir(path.db.star)
    mkdir(path.db.nm)
    mkdir(path.db.hd)
    mkdir(path.db.mx)
    mkdir(path.db.ex)
    mkdir(path.db.club)
    mkdir(path.db.mission)
    mkdir(path.db.master)
    mkdir(path.img.root)
    mkdir(path.img.icon)
    mkdir(path.img.star)
    mkdir(path.img.pop)
    mkdir(path.img.club)
    mkdir(path.img.mission)
