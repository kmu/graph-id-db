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

    # from graph_id.cpp.imports import graph_id_cpp
    import graph_id_cpp
    from graphid_dev.core.graphid import GraphID
    from pymatgen.core.structure import Structure

    structure = Structure.from_file(cif)
    structure.merge_sites(mode="delete")

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
    distance_clustering_id = distance_clustering_gen.get_long_distance_id(structure)

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
    with open(f"{out_dir}/{data_source_id}.json", "w") as f:
        json.dump(json_dict, f)

    # structure.to(f"{out_dir}/cifs/{data_source_id}.cif")

    return json_dict


# iza = IZARester()
# codes = iza.get_code_list(defect_free=True)
# print(codes)


class MiraiProvider(GridEngineProvider):
    def _write_submit_script(self, template, script_filename, job_name, configs):
        """Generate submit script and write it to a file.

        Args:
              - template (string) : The template string to be used for the writing submit script
              - script_filename (string) : Name of the submit script
              - job_name (string) : job name
              - configs (dict) : configs that get pushed into the template

        Returns:
              - True: on success

        Raises:
              SchedulerMissingArgs : If template is missing args
              ScriptPathError : Unable to write submit script out
        """

        def remove_lines_having_keyword_from(input_str, keyword="#SBATCH --nodes="):
            lines = input_str.split("\n")
            result = [line for line in lines if keyword not in line]
            return "\n".join(result)

        try:
            submit_script = Template(template).substitute(jobname=job_name, **configs)
            # submit_script = submit_script.replace("#SBATCH --nodes=1", "")
            # submit_script = remove_lines_having_keyword_from(submit_script, "#SBATCH --nodes=")
            # submit_script = remove_lines_having_keyword_from(submit_script, "#SBATCH --time=")
            submit_script = remove_lines_having_keyword_from(
                submit_script, "#$ -l h_rt="
            )
            with open(script_filename, "w") as f:
                f.write(submit_script)

        except KeyError as e:
            logger.error("Missing keys for submit script : %s", e)
            raise SchedulerMissingArgs(e.args, self.label)

        except OSError as e:
            logger.error("Failed writing to submit script: %s", script_filename)
            raise ScriptPathError(script_filename, e)
        except Exception as e:
            print("Template : ", template)
            print("Args : ", job_name)
            print("Kwargs : ", configs)
            logger.error("Uncategorized error: %s", e)
            raise
        return True


def mirai_config(
    qnode: str,
    max_blocks: int = 1,
    core_per_block: int = 1,
    max_workers: int = 1,
    run_dir: str = "runinfo",
) -> Config:
    return Config(
        executors=[
            HighThroughputExecutor(
                label="mirai",
                # max_workers=max_workers,
                provider=MiraiProvider(
                    launcher=SimpleLauncher(),  # command as-is. This works.
                    channel=LocalChannel(),
                    nodes_per_block=1,
                    init_blocks=1,
                    max_blocks=max_blocks,
                    scheduler_options=f"""#$ -N mp
#$ -q {qnode},
#$ -pe impi {core_per_block}""",  # Input your scheduler_options if needed
                    worker_init="""
conda activate matf
""",
                ),
            ),
        ],
        app_cache=True,
        run_dir=run_dir,
    )


parsl_config = mirai_config(
    qnode="bosch.q@compute-4-1",
    max_blocks=4,
)
# parsl_config.checkpoint_files = get_all_checkpoints()
dfk = parsl.load(parsl_config)

# parser = argparse.ArgumentParser()
# parser.add_argument(
#     "--mirai_max_blocks",
#     type=str,
#     default="mczeo56:1",
# )
# args = parser.parse_args()

# gen = ParslConfigGenerator(mirai_max_blocks=args.mirai_max_blocks)
# config = gen.get_config()
# dfk = parsl.load(config)

futures = []

# Create output directory
out_dir = Path("raw/mp/id_json")
out_dir.mkdir(parents=True, exist_ok=True)

cifs = glob.glob("/home/tanimoto/graphid-db/raw/mp/cifs/*.cif")
pattern = r"mp-\d+"
for cif in cifs:
    mp_id = cif.replace("/home/tanimoto/graphid-db/raw/mp/cifs/", "").replace(
        ".cif", ""
    )

    # Call the compute_graphids function with proper arguments
    f = compute_graphids(
        cif=cif,
        data_source="MP",
        data_source_id=mp_id,
        data_source_url=f"https://next-gen.materialsproject.org/materials/{mp_id}",
        out_dir=str(out_dir),
    )
    futures.append(f)

# Wait for all tasks to complete
try:
    results = [f.result() for f in futures]
    print(f"Completed processing {len(results)} mp structures")
except Exception as e:
    print(f"Error processing mp structures: {e}")
finally:
    # Clean up Parsl DFK
    dfk.cleanup()
