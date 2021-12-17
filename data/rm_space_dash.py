from pathlib import Path
import os.path as osp
import argparse


def main(args):
    for gt_file in args.gt_files:
        with open(gt_file, "r") as f:
            content = f.read()

        output = ""
        content_lines = content.split("\n")
        for content_line in content_lines:
            if content_line:
                filename, gt = content_line.split("\t")
                gt = gt.replace(" ", "") if args.nospace else gt
                gt = gt.replace("-", "") if args.nodash else gt
                output += f"{filename}\t{gt}\n"

        store_file_name = Path(gt_file).stem
        store_file_name = store_file_name + "_nospace" if args.nospace else store_file_name
        store_file_name = store_file_name + "_nodash" if args.nodash else store_file_name
        store_file_name += ".txt"
        with open(osp.join(args.gt_root, store_file_name), "w") as f:
            f.write(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--gt_root", type=str, help="root directory name of ground truth.")
    parser.add_argument("--gt_files", type=str, nargs="+", help="root directory name of ground truth.")
    parser.add_argument("--nospace", action="store_true", help="if true, remove blank space.")
    parser.add_argument("--nodash", action="store_true", help="if true, remove dash character.")

    args = parser.parse_args()
    main(args)
