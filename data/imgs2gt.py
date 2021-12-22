import os.path as osp
import argparse
from glob import glob
from pathlib import Path


def main(args):
    output = ""
    img_files = glob(osp.join(args.img_dir, "*.jpg"))

    for img_file in img_files:
        img_file = img_file.replace(f"{args.img_dir}/", "")
        gt = Path(img_file).stem
        output += f"{img_file}\t{gt}\n"

    with open(osp.join(args.img_dir, "gt.txt"), "w") as f:
        f.write(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--img_dir", type=str, help="directory having image files.")

    args = parser.parse_args()
    args.img_dir = args.img_dir.replace("/", "")

    main(args)


