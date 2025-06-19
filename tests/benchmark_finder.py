import time
import json
import pandas as pd
from pathlib import Path
from typing import Any, Optional

from graphid_db.finder import Finder

TEST_PATH = Path(__file__).parent / "test_files"
graphids_path = TEST_PATH / "graphids.csv"
graphids_df = pd.read_csv(graphids_path)

start_time = time.time()
for graphid in graphids_df["graphid"]:
    finder = Finder()
    docs = finder.find(graphid)
    print(f"Hash: {graphid}, found {len(docs)} entries")
end_time = time.time()

print(f"Elapse time = {end_time - start_time} s")
"""
json -> 16 s
orjson -> 0.92 s
"""
