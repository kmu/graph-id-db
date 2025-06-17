import json
import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path

from graphid_db.finder import Finder, DB_PATH


def test_ac():
    finder = Finder()
    docs = finder.find("Ac3-7c22ad86c9eb7999")
    assert docs[0]["graph_id_type"] == "topo_md_id"
    assert docs[0]["proprietary_id"] == "mp-1183057"
    assert docs[0]["datasource"] == "MP"
    assert docs[0]["url"] == "https://next-gen.materialsproject.org/materials/mp-1183057"
    assert docs[0]["filehash"] == "ebefafe6539be2b6"
    assert len(docs) == 1

def test_not_found_ac():
    finder = Finder()
    docs = finder.find("Ac3-xxxx")
    assert docs is None


def test_not_found_not_composition():
    finder = Finder()
    docs = finder.find("Xx-7c22ad86c9eb7999")
    assert docs is None
