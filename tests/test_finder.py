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
