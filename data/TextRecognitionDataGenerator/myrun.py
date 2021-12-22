import argparse
import random
import os.path as osp
import string
import secrets
from PIL import Image
from pathlib import Path
from pprint import pprint

from trdg.generators import (
    GeneratorFromDict,
    GeneratorFromRandom,
    GeneratorFromStrings,
    GeneratorFromWikipedia,
)


TAG_GEN_DICT = "".join([string.ascii_uppercase] + [string.digits] * 3 + [' ']*10 + ["#()-"])



def first_char_is_dash(string:str):
    return string[0] == "-"

def last_char_is_dash(string:str):
    return string[-1] == "-"

def is_contain_dash(string:str):
    return "-" in string

def is_not_contain_dash(string:str):
    return not is_contain_dash(string)

def is_contain_space(string:str):
    return " " in string

def is_not_contain_space(string:str):
    return not is_contain_space(string)

def must_re_create(random_string:str, args):
    return first_char_is_dash(random_string) or \
            last_char_is_dash(random_string) or \
            (args.dash and is_not_contain_dash(random_string)) or \
            (args.space and is_not_contain_space(random_string)) or \
            (args.nospace and is_contain_space(random_string))


def get_random_string(rand_len:int, args):
    random_string = "-"

    while must_re_create(random_string, args):
        random_string = ''.join(secrets.choice(TAG_GEN_DICT) for _ in range(rand_len))
        random_string = random_string.strip()

    return random_string


def main(args):
    total_string = args.n

    # 영어 대문자, 숫자, -, 공백을 포함한 랜덤 문자열 생성
    rand_lens = [random.randint(args.min_len, args.max_len) for _ in range(total_string)]
    results = [get_random_string(rand_len, args) for rand_len in rand_lens]

    # 이미지 저장을 위한 syns_images 생성
    Path(args.dst_dir).mkdir(parents=False, exist_ok=True)

    # The generators use the same arguments as the CLI, only as parameters
    generator = GeneratorFromStrings(
        strings=results,    # 문자열
        count=total_string, # 생성할 이미지 개수
        size=92,            # 이미지 가로 길이
        # distorsion_type = 3,  # 왜곡 정도
        blur=args.blur_power,             # 흐림 정도
        random_blur=args.blur,   # 흐림 랜덤
        text_color='#000000,#888888', # 색상 랜덤

        skewing_angle=args.angle,
        random_skew=True,
        background_type=2,
        orientation=0, # 0: horizonta, 1: vertical

        distorsion_type=0,
        distorsion_orientation=0,
        alignment=0,
        space_width=1.0,
        character_spacing=0,
        margins=(5, 5, 5, 5),
        fit=True,
        word_split=True,
        image_mode="RGB",
    )

    for img, label in generator:
        # print(label)                  # 문자열 출력
        img.save(osp.join(args.dst_dir,f'{label}.jpg')) # 이미지 저장


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", "--num_of_generated_strings", type=int, default=10, help="the number of generated strings.")
    parser.add_argument("--min_len", type=int, default=6, help="the max length of generated strings.")
    parser.add_argument("--max_len", type=int, default=20, help="the min length of generated strings.")
    parser.add_argument("--dash", action='store_true', help="if True, dash character must be inserted.")
    parser.add_argument("--blur", action='store_false', help="if False, character always be blured.")
    parser.add_argument("--blur_power", type=int, default=2, help="Set blur power (recommanded max is 7)")
    parser.add_argument("--space", action='store_true', help="if True, space character must be inserted.")
    parser.add_argument("--nospace", action='store_true', help="if True, space character must be NOT inserted.")
    parser.add_argument("--angle", type=int, default=0, help="set angle of text")
    parser.add_argument("--dst_dir", type=str, default="syns", help="destination directory of generated images.")

    args = parser.parse_args()
    main(args)


