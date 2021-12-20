from array import array
import io
import numpy as np
from PIL import Image

import albumentations
import albumentations.pytorch
import torch
import streamlit as st
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials



credentials_dict = {
    'type': 'service_account',
    'client_id': st.secrets['gcp']['client_id'],
    'client_email': st.secrets['gcp']['client_email'],
    'private_key_id': st.secrets['gcp']['private_key_id'],
    'private_key': st.secrets['gcp']['private_key'],
}
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials_dict
)
    
def send_to_bucket(image_name:str, image_bytes:bytes):
    client = storage.Client(credentials=credentials, project=st.secrets['gcp']['project_id'])
    bucket = client.get_bucket(st.secrets['gcp']['bucket'])
    bucket.blob(image_name).upload_from_string(image_bytes)
    image_url = bucket.blob(image_name).public_url
    return image_url

def bring_from_bucket(image_name:str):
    client = storage.Client(credentials=credentials, project=st.secrets['gcp']['project_id'])
    bucket = client.get_bucket(st.secrets['gcp']['bucket'])
    bringImage = bucket.blob(image_name).download_as_string()
    return bringImage

def get_naver_api(label:str):
    import urllib.request
    import json
    client_id = st.secrets['gcp']['X-Naver-Client-Id']
    client_secret = st.secrets['gcp']['X-Naver-Client-Secret']
    print("client_id",client_id)
    query = label
    query = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/shop?query=" + query
    request = urllib.request.Request(url)
    request.add_header('X-Naver-Client-Id', client_id)
    request.add_header('X-Naver-Client-Secret', client_secret)
    response = urllib.request.urlopen(request)
    return response

if __name__ == "__main__":
    get_naver_api("343938013")

