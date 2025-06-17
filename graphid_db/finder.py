import json
from pathlib import Path
from typing import Any, Dict, Optional

from pymatgen.core import Composition

DB_PATH = Path(__file__).parent.parent / "raw/id_jsons"


class Finder:
    def find(self, graph_id: str) -> Optional[Dict[str, Any]]:
        if "-" in graph_id:
            composition_str, graph_hash = graph_id.split("-")
            composition = Composition(composition_str)

            db_path = (
                DB_PATH
                / composition.reduced_formula
                / f"{composition.formula}.json"
            )
            if db_path.exists():
                with open(db_path) as f:
                    docs = json.load(f)
                    return docs.get(graph_hash)

            return None
        else:
            return None
