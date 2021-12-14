import torch
import torch.nn as nn
import torch.nn.functional as F
import streamlit as st
from model import MyEfficientNet
from utils import transform_image

import io
import os
import yaml
from PIL import Image
from typing import Tuple, List

from fastapi import FastAPI, File, UploadFile


app = FastAPI()


@app.post("/prediction/")
async def get_prediction(files: List[UploadFile] = File(...)):

    image_bytes = files[0].file.read()
    image_name = files[0].filename
    image = Image.open(io.BytesIO(image_bytes))

    if not os.path.exists("./tmp"):
        os.mkdir("./tmp")
    image.save(f"./tmp/{image_name}.jpg", "PNG")

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

    return {"label": label, "conf":conf}


def main():
    import uvicorn
    uvicorn.run("back:app", host="0.0.0.0", port=8501, reload=True)


if __name__ == "__main__":
    main()

