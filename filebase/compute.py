from pathlib import Path
import logging
import parsl
from parsl.app.app import python_app

from parsl.config import Config
import glob

from parsl.channels import LocalChannel
from parsl.executors import HighThroughputExecutor
from parsl.launchers import SimpleLauncher
from string import Template

from parsl.providers import GridEngineProvider
from parsl.providers.errors import SchedulerMissingArgs, ScriptPathError

logger = logging.getLogger(__name__)

@python_app(cache=True, ignore_for_cache=["out_dir"])
def compute_graphids(
    cif: str, data_source: str, data_source_id: str, data_source_url: str, out_dir="."
):
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
    from graphid_dev.core.graphid import GraphID
    from pymatgen.core.structure import Structure

    structure = Structure.from_str(cif, fmt="cif")
    structure.merge_sites(mode="delete")

    # An error occurs in MinimumDistanceNN if len(neighs_dists) == 0 
    for i in range(len(structure)):
        site = structure[i]
        neighs_dists = structure.get_neighbors(site, 10.0)

        if len(neighs_dists) == 0:
            json_dict = {
                "md_id": "",
                "topo_md_id": "",
                "dc_id": "",
                "data_source": data_source,
                "data_source_id": data_source_id,
                "data_source_url": data_source_url,
            }
            # Write JSON output file
            with open(f"{out_dir}/{data_source_id}.json", "w") as f:
                json.dump(json_dict, f)

            return json_dict

    gen = GraphID(digest_size=8)
    minimum_distance_id = gen.get_id(structure)

    topo_minimum_distance_id = graph_id_cpp.GraphIDGenerator(topology_only=True, digest_size=8).get_id(
        structure
    )

    distance_clustering_gen = graph_id_cpp.GraphIDGenerator(rank_k=3, cutoff=6.0, digest_size=8)
    distance_clustering_id = distance_clustering_gen.get_id(structure)

    # JSON dictionary with graph IDs and metadata
    json_dict = {
        "md_id": minimum_distance_id,
        "topo_md_id": topo_minimum_distance_id,
        "dc_id": distance_clustering_id,
        "data_source": data_source,
        "data_source_id": data_source_id,
        "data_source_url": data_source_url,
    }
    with open(f"{out_dir}/{data_source_id}.json", "w") as f:  # noqa: PTH123
        json.dump(json_dict, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir", type=str, required=True, help="Directory containing CIF files"
    )
    parser.add_argument("--data_source", type=str, required=True, help="Data source")
    parser.add_argument(
        "--data_source_url", type=str, required=True, help="Data source URL"
    )
    parser.add_argument(
        "--out_dir", type=str, default=".", help="Output directory for JSON files"
    )

    args = parser.parse_args()
    dfk = parsl.dfk()

    cif_dir = Path(args.dir)
    if not cif_dir.exists():
        raise ValueError(f"Directory {cif_dir} does not exist")  # noqa: TRY003, EM102

    # Create output directory
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    cif_files = list(cif_dir.glob("**/*.cif"))
    print(f"Found {len(cif_files)} CIF files in {cif_dir}")

    futures = []
    for cif_file in cif_files:
        path = Path(cif_file)
        with path.open() as f:
            cif = f.read()
        futures.append(
            compute_graphids(
                cif=cif,
                data_source=args.data_source,
                data_source_id=cif_file.stem,
                data_source_url=args.data_source_url,
                out_dir=args.out_dir,
            ),
        )

    results = [future.result() for future in futures]
    print(f"Completed processing {len(results)} structures")

    dfk.cleanup()
