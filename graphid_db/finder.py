from pathlib import Path
from typing import Optional

import orjson

DB_PATH = Path(__file__).parent.parent / "raw/id_jsons"


class Finder:
    def find(self, graph_id: str) -> Optional[dict[str, list[dict[str, str]]]]:
        dir_name = graph_id[:2]
        file_name = graph_id[:4]

        db_path = DB_PATH / dir_name / f"{file_name}.json"
        if db_path.exists():
            with open(db_path) as f:
                docs = orjson.loads(f.read())
                return docs.get(graph_id)

        return None
