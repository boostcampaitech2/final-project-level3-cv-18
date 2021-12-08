import streamlit as st
from streamlit_cropper import st_cropper

import io
import os
import yaml
import time

from PIL import Image

from predict import load_model, get_prediction

from confirm_button_hack import cache_on_button_press

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

# st.set_option('deprecation.showfileUploaderEncoding', False)


def main():
    st.title("Shoes product number OCR")

    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    # 모델 불러오기, 시간이 오래 걸리는 작업부터
    # st.write("Classifying...")
    # model = load_model()
    # model.eval()

    st.header("Image Uploader")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg","png"])
    realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
    box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
    aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["16:9", "Free"])
    aspect_dict = {"16:9": (16,9),
                    "Free": None}
    aspect_ratio = aspect_dict[aspect_choice]

    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_bytes))

        if not realtime_update:
            st.write("Double click to save crop")
        cropped_img = st_cropper(image, realtime_update=realtime_update, box_color=box_color, aspect_ratio=aspect_ratio)

        # Manipulate cropped image at will
        st.write("Preview")
        _ = cropped_img.thumbnail((150,150))
        st.image(cropped_img)

        # 모델에 이미지 입력 (여기서부터 안 됨)
        # cropped_img = cropped_img.save(io.BytesIO(), 'PNG')

        # 추론 시작
        # st.write("Classifying...")
        # _, y_hat = get_prediction(model, cropped_img)
        # label = config['classes'][y_hat.item()]

        # 추론 결과 반영
        # st.write(f'label is {label}')
main()


# 기존에 있던 로그인 코드 / 로깅 기능을 위해 남겨두나 로깅 기능 추가는 시간제약으로 어려울 듯...
# @cache_on_button_press('Authenticate')
# def authenticate(password) ->bool:
#     print(type(password))
#     return password == root_password


# password = st.text_input('password', type="password")

# if authenticate(password):
#     st.success('You are authenticated!')
#     main()
# else:
#     st.error('The password is invalid.')