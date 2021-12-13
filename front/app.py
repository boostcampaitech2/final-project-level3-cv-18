import streamlit as st
from streamlit_cropper import st_cropper

import io
import os
import yaml
import time

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
    
    # 모델 불러오기, 시간이 오래 걸리는 작업부터
    # st.write("Classifying...")
    # model = load_model()
    # model.eval()

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
        cropped_img = st_cropper(image, box_color=box_color, aspect_ratio=aspect_ratio)

        # Manipulate cropped image at will
        st.write("Preview")
        # cropped_img.thumbnail((150,150))
        st.image(cropped_img)

        # 모델에 이미지 입력 (여기서부터 안 됨)
        cropped_img = cropped_img.save(io.BytesIO(), 'PNG')

        # 추론 시작
        # st.write("Classifying...")
        # _, y_hat = get_prediction(model, cropped_img)
        # label = config['classes'][y_hat.item()]

        # 추론 결과 반영
        # st.write(f'label is {label}')
        
main()