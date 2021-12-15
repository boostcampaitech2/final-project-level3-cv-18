import json
import os
import os.path as osp
from glob import glob

import pandas as pd
from pprint import pprint


CAMPER_IDS = ["T2035", "T2042", "T2113", "T2157", "T2213", "T2260"]


def get_output_from_json(camper_id: str, anno_file:str):
    output = ""
    with open(anno_file, "r") as f:
        content = json.load(f)
    for filename in content:
        product_no = content[filename]["regions"][0]["region_attributes"]["product_no"]
        output += f"{camper_id}/{filename}\t{product_no}\n"

    return output.strip()


def get_output_from_csv(camper_id: str, anno_file:str):
    output = ""

    content = pd.read_csv(anno_file)
    filenames = content["filename"].tolist()
    region_attributes = content["region_attributes"].apply(json.loads).tolist()
    for filename, region_attr in zip(filenames, region_attributes):
        if not region_attr:
            continue

        product_no = region_attr["product_no"]

        if "###" in product_no:
            continue
        output += f"{camper_id}/{filename}\t{product_no}\n"

    return output.strip()


def get_output_from_xlsx(camper_id: str, anno_file:str):
    output = ""

    content = pd.read_excel(anno_file, engine="openpyxl")
    content = content[content["region_attributes"].apply(str) != "nan"]

    filenames = content["filename"].tolist()
    region_attributes = content["region_attributes"].apply(json.loads).tolist()
    for filename, region_attr in zip(filenames, region_attributes):
        if not region_attr:
            continue

        product_no = region_attr["product_no"]

        if "###" in product_no:
            continue
        output += f"{camper_id}/{filename}\t{product_no}\n"

    return output.strip()


if __name__ == "__main__":
    output = ""
    for camper_id in CAMPER_IDS:
        anno_files = glob(osp.join("anno", f"{camper_id}*"))

        for anno_file in anno_files:
            if "json" in anno_file:
                output += get_output_from_json(camper_id, anno_file)
            elif "csv" in anno_file:
                output += get_output_from_csv(camper_id, anno_file)
            elif "xlsx" in anno_file:
                output += get_output_from_xlsx(camper_id, anno_file)

            break

    with open("gt.txt", "w") as f:
        f.write(output)

