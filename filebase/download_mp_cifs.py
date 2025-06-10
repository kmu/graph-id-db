from tqdm import tqdm
from icecream import ic
from mp_api.client import MPRester

api_key = "BuHSswwUfhwgUUI99dgY6wsNn9GM3jU1"

cif_dir = "/home/tanimoto/graphid-db/raw/mp/cifs"

# MPResterを初期化
with MPRester(api_key) as mpr:
    # すべての材料のIDを取得
    materials = mpr.materials.search()
    ic(len(materials)) # 154879

    # # 各材料のCIFファイルをダウンロード
    # for material in tqdm(materials):
    #     material_id = material.material_id
    #     structure = mpr.get_structure_by_material_id(material_id)
    #     cif_filename = f"{cif_dir}/{material_id}.cif"
    #     structure.to(fmt="cif", filename=cif_filename)
    #     print(f"CIFファイルが {cif_filename} としてダウンロードされました")
