import torch
import torch.nn as nn
import torch.nn.functional as F
import streamlit as st
from model import MyEfficientNet
from utils import transform_image

import os
import yaml
from PIL import Image
from typing import Tuple



@st.cache
def load_model(opt) -> nn.Module:

    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = Model(opt).to(device)

    state_dict = torch.load(config['model_path'], map_location=device)
    pretrained_model_state_dict = {}
    for k, v in state_dict.items():
        k = k.replace("module.", "")
        pretrained_model_state_dict[k] = v

    model.load_state_dict(pretrained_model_state_dict)

    return model


def get_prediction(image: Image) -> Tuple[torch.Tensor, torch.Tensor]:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if not os.path.exists("./tmp"):
        os.mkdir("./tmp")

    image.save("./tmp/tmp.jpg", "PNG")

    os.system("CUDA_VISIBLE_DEVICES=0 python3 ../deep-text-recognition-benchmark/demo.py \
--Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn \
--image_folder ./tmp/ \
--saved_model ./model.pth > ./tmp/tmp.txt")

    with open("./tmp/tmp.txt") as f:
        output = f.read()

    row = output.split("--------------------------------------------------------------------------------")[-1]
    row = row.split('\t')

    filename = row[0].strip()
    label = row[1].strip()
    conf = row[2].strip()

    os.system("rm -rf ./tmp")

    return label, conf


#def get_prediction(model:MyEfficientNet, image_bytes: bytes) -> Tuple[torch.Tensor, torch.Tensor]:
#    tensor = transform_image(image_bytes=image_bytes)
#    outputs = model.forward(tensor)
#    _, y_hat = outputs.max(1)
#    return tensor, y_hat
