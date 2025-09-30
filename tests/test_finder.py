from graph_id_db.finder import Finder


def test_hash():
    finder = Finder()
    docs = finder.find("7c22ad86c9eb7999")
    assert docs[0]["graph_id_type"] == "topo_md_id"
    assert docs[0]["proprietary_id"] == "mp-1183057"
    assert docs[0]["datasource"] == "MP"
    assert (
        docs[0]["url"]
        == "https://next-gen.materialsproject.org/materials/mp-1183057"
    )
    assert docs[0]["filehash"] == "ebefafe6539be2b6"
    assert len(docs) == 47


def test_not_found_hash():
    finder = Finder()
    docs = finder.find("xxxx")
    assert docs == []


def test_aflow():
    finder = Finder()

    fast_docs = finder.find("0000c690d6bd9179", is_fast=True)
    aflow_docs = finder.find("0000c690d6bd9179")

    assert fast_docs == []
    assert aflow_docs[0]["graph_id_type"] == "dc_id"
    assert aflow_docs[0]["proprietary_id"] == "aflow:06966bc7b36b2343"
    assert aflow_docs[0]["datasource"] == "AFLOW"
    assert (
        aflow_docs[0]["url"]
        == "https://aflow.org/material/?id=aflow:06966bc7b36b2343"
    )
    assert aflow_docs[0]["filehash"] == "3ecb4cc4656f22e6c424f3fbaa0d2d4e62cfe1f827857072197ca3a31db16b78"
    assert len(aflow_docs) == 2
