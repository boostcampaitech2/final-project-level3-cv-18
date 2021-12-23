import torch
import torch.nn as nn
import torch.nn.functional as F

import io
import os
import os.path as osp
import shutil
from PIL import Image
from typing import Tuple, List

from fastapi import FastAPI, File, UploadFile
from inference.inference import inference
from container import ModelContainer


app = FastAPI()


@app.post("/prediction/")
async def get_prediction(files: List[UploadFile] = File(...)):

    image_bytes = files[0].file.read()
    image_name = files[0].filename
    image = Image.open(io.BytesIO(image_bytes))

    if not osp.exists("./tmp"):
        os.mkdir("./tmp")
        image.save("./tmp/tmp.jpg", "PNG")

    model_container = ModelContainer()
    model, converter, opt = model_container()
    img_names, preds, confidence_scores = inference(model, converter, opt)
    label, confidence_score = preds[0], confidence_scores[0]

    if osp.exists("./tmp"):
        shutil.rmtree("./tmp")

    return {"label": label, "conf": confidence_score}


def main():
    import uvicorn
#    uvicorn.run("back:app", host="0.0.0.0", port=8501, reload=True)
    uvicorn.run("back:app", host="0.0.0.0", port=6006, reload=True)


if __name__ == "__main__":
    main()

