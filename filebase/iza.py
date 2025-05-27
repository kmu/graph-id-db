import argparse
from pathlib import Path

import parsl
from chemsys.pymatgen.ext.iza import IZARester
from parsl.app.app import python_app
from parsl_configs.config.config_mrok import ParslConfigGenerator


@python_app(cache=True, ignore_for_cache=["out_dir"])
def compute_graphids(cif: str, data_source: str, data_source_id: str, data_source_url: str, out_dir="."):
    """
    Compute graph IDs for a structure given as CIF string.

    Args:
        cif: CIF string representing the structure
        data_source: Name of the data source
        data_source_id: ID of the structure in the data source
        data_source_url: URL to the structure in the data source
        out_dir: Directory to write the output JSON file
    """
    import json

    import graph_id_cpp
    from pymatgen.core.structure import Structure

    structure = Structure.from_str(cif, fmt="cif")
    structure.merge_sites(mode="delete")
    gen = graph_id_cpp.GraphIDGenerator()
    minimum_distance_id = gen.get_id(structure)

    topo_minimum_distance_id = graph_id_cpp.GraphIDGenerator(topology_only=True).get_id(structure)

    distance_clustering_id = ""

    # JSON dictionary with graph IDs and metadata
    json_dict = {
        "md_id": minimum_distance_id,
        "topo_md_id": topo_minimum_distance_id,
        "dc_id": distance_clustering_id,
        "data_source": data_source,
        "data_source_id": data_source_id,
        "data_source_url": data_source_url,
    }

    # Write JSON output file
    path = Path(f"{out_dir}/{data_source_id}.json")
    with path.open("w") as f:
        json.dump(json_dict, f)

    return json_dict


iza = IZARester()
codes = iza.get_code_list(defect_free=True)
print(codes)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--mirai_max_blocks",
    type=str,
    default="mczeo56:1",
)
args = parser.parse_args()

gen = ParslConfigGenerator(mirai_max_blocks=args.mirai_max_blocks)
config = gen.get_config()
dfk = parsl.load(config)

futures = []

# Create output directory
out_dir = Path("raw/iza")
out_dir.mkdir(parents=True, exist_ok=True)

for c in codes:
    cif_content = iza.get_cif_str_by_code(c)

    # Call the compute_graphids function with proper arguments
    f = compute_graphids(
        cif=cif_content,
        data_source="International Zeolite Association",
        data_source_id=c,
        data_source_url=f"https://asia.iza-structure.org/IZA-SC/framework.php?STC={c}",
        out_dir=str(out_dir),
    )
    futures.append(f)

# Wait for all tasks to complete
try:
    results = [f.result() for f in futures]
    print(f"Completed processing {len(results)} IZA structures")
except Exception as e:  # noqa: BLE001
    print(f"Error processing IZA structures: {e}")
finally:
    # Clean up Parsl DFK
    dfk.cleanup()
