from typing import Dict
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

from confirm_button_hack import cache_on_button_press
from utils import send_to_bucket,get_naver_api
from uuid import uuid1
from datetime import datetime

st.set_page_config(page_title="Shoes product number OCR", page_icon=":athletic_shoe:", layout="centered")

# 상품 정보 출력해주는 함수
def product_info_print(get_item_info):
    st.write("상품명",get_item_info['title'])
    st.write("최저가",get_item_info['lprice'])
    st.write("상품 보러가기",get_item_info['link'])
    st.image(get_item_info['image'])


# model 결과 저장해주기 위해서 cache로 따로 빼둠
@st.cache()
def get_inference(files):
    start = time.time()
    #response = requests.post(f"http://{os.environ['BACKEND_HOST']}:8501/prediction/", files=files)
    response = requests.post(f"http://localhost:8501/prediction/", files=files)

    end = time.time()
    tm = end-start
    return response,tm

def main():

    st.title(":athletic_shoe: Shoes product number OCR!!")


    st.header("Uploaded Image")
    uploaded_file = st.sidebar.file_uploader("Choose an image", type=["jpg", "jpeg","png"])
    realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
    box_color = st.sidebar.color_picker(label="Box Color", value='#F00000')
    aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["Free"])
    aspect_dict = {"Free": None}
    aspect_ratio = aspect_dict[aspect_choice]

    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_bytes))
        if not realtime_update:
            st.write("Double click to save crop")
        cropped_img = st_cropper(image, box_color=box_color, aspect_ratio=aspect_ratio,realtime_update=realtime_update).convert("L")

        # Manipulate cropped image at will
        st.write("Preview")
        st.image(cropped_img)

        # 모델에 이미지 입력
        cropped_img_byte = io.BytesIO()
        cropped_img.save(cropped_img_byte, format='PNG')
        cropped_img_byte = cropped_img_byte.getvalue()
        st.write("Classifying...")
        files = [('files', (uploaded_file.name, cropped_img_byte, uploaded_file.type))]

        response,tm = get_inference(files)
        st.write(response.status_code)
        label, confidence_score = response.json().values()
        st.write(response.json())

        # 추론 결과 반영

        st.subheader(f'label is {label}, {confidence_score}')
        st.write(f"inferance time : {tm:.2f}second")
        st.subheader("is product code incorrected?")
        label = st.text_input("input correct product code",label)

        # naver api 정보 가져오기
        with st.expander("상품 정보 확인하기"):
             get_item_info = get_naver_api(label = label)
             if get_item_info == "Not Exist":
                 st.write("Can't find product")
             else :
                 product_info_print(get_item_info)
                 send_to_bucket(image_id=uuid1(),label = label,image_bytes=cropped_img_byte,date=datetime.now())



if __name__ == "__main__":
    main()

