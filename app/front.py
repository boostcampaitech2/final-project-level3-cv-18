import streamlit as st
from streamlit_cropper import st_cropper

import io
import os
import yaml
import time
import argparse
import requests

import numpy as np
from PIL import Image

from predict import load_model, get_prediction

from confirm_button_hack import cache_on_button_press

# SETTING PAGE CONFIG TO WIDE MODE - 탭 제목
# st.set_page_config(layout="wide")
st.set_page_config(page_title="Shoes product number OCR", page_icon=":athletic_shoe:", layout="centered")
# st.set_option('deprecation.showfileUploaderEncoding', False)


def main():

    st.title(":athletic_shoe: Shoes product number OCR!!")

    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    st.header("Uploaded Image")
    uploaded_file = st.sidebar.file_uploader("Choose an image", type=["jpg", "jpeg","png"])
    # realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
    box_color = st.sidebar.color_picker(label="Box Color", value='#F00000')
    aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
    aspect_dict = {"1:1": (1,1),
                    "16:9": (16,9),
                    "4:3": (4,3),
                    "2:3": (2,3),
                    "Free": None}
    aspect_ratio = aspect_dict[aspect_choice]

    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_bytes))

        # if not realtime_update:
        #     st.write("Double click to save crop")
        cropped_img = st_cropper(image, box_color=box_color, aspect_ratio=aspect_ratio).convert("L")

        # Manipulate cropped image at will
        st.write("Preview")
        # cropped_img.thumbnail((150,150))
        st.image(cropped_img)

        # 모델에 이미지 입력 (여기서부터 안 됨)

        cropped_img_byte = io.BytesIO()
        cropped_img.save(cropped_img_byte, format='PNG')
        cropped_img_byte = cropped_img_byte.getvalue()
        #st.write(np.array(cropped_img).shape)
        # 추론 시작
        st.write("Classifying...")
        files = [('files', (uploaded_file.name, cropped_img_byte, uploaded_file.type))]

        #label, confidence_score = get_prediction(cropped_img)
        response = requests.post("http://localhost:8501/prediction/", files=files)
        st.write(response.status_code)
        label, confidence_score = response.json().values()

        # 추론 결과 반영
        st.write(f'label is {label}, {confidence_score}')


if __name__ == "__main__":
    main()


