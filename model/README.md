# For our works

## 0. Installation
```bash
pip install -r requirement.txt

apt-get update
apt-get install libmagickwand-dev
```

## 1. Transform our data into LMDB data.
```bash
$ python3 create_lmdb_dataset.py \
--inputPath ${IMAGE_ROOT}/ --gtFile ${IMAGE_ROOT}/gt.txt \
--outputPath result
```
> Transfromed files is created in the directory named "result".

## 2. Train 
Fine-tune with pretrained model.
- [Download link of Clova AI's pretrained models](https://www.dropbox.com/sh/j3xmli4di1zuv3s/AAArdcPgz7UFxIHUuKNOeKv_a?dl=0)
- [Download link of ViTSTR pretrained models](https://github.com/oikosohn/deep-text-recognition-benchmark-1)
```bash
# training Clova AI best accuracy model TRBA
CUDA_VISIBLE_DEVICES=0 python3 train.py \
--train_data result.traindata/ --valid_data result.validdata/ \
----Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn \
--batch_size 32 --num_iter 5000 --valInterval 1000 --input_channel 1 \
--saved_model ./pretrained_models/TPS-ResNet-BiLSTM-Attn.pth 
```
> Must match Transformation, FeatureExtraction, SequenceModeling, Prediction with saved_model.

```bash
# training ViTSTR tiny
CUDA_VISIBLE_DEVICES=0 python3 train.py \
--train_data result.traindata/ --valid_data result.validdata/ \
--Transformation None --FeatureExtraction None  --SequenceModeling None --Prediction None --Transformer \
--TransformerModel vitstr_tiny_patch16_224 \
--batch_size 32 --num_iter 5000 --valInterval 1000 --input_channel 1 \
--imgH 224 --imgW 224 \
--saved_model ./pretrained_models/vitstr_tiny_patch16_224.pth
```

## 3. Test trained model
```bash
# testing None-VGG-None-CTC
CUDA_VISIBLE_DEVICES=0 python3 test.py \
--eval_data data_lmdb_release/evaluation --benchmark_all_eval \
--Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn \
--saved_model <path_to/best_accuracy.pth>
```

```bash
# testing ViTSTR tiny
CUDA_VISIBLE_DEVICES=0 python3 test.py --eval_data ./data/teamdata_nospace  \
--Transformation None --FeatureExtraction None \
--SequenceModeling None --Prediction None --Transformer \
--TransformerModel=vitstr_tiny_patch16_224 \
--sensitive --data_filtering_off  --imgH 224 --imgW 224 \
--saved_model <path_to/best_accuracy.pth>
```

## 4. Move trained model
```bash
$ mv trained_model.pth ${BACKEND_DIR}
```

## Citation
Please consider citing this work in your publications if it helps your research.
```
@inproceedings{baek2019STRcomparisons,
  title={What Is Wrong With Scene Text Recognition Model Comparisons? Dataset and Model Analysis},
  author={Baek, Jeonghun and Kim, Geewook and Lee, Junyeop and Park, Sungrae and Han, Dongyoon and Yun, Sangdoo and Oh, Seong Joon and Lee, Hwalsuk},
  booktitle = {International Conference on Computer Vision (ICCV)},
  year={2019},
  pubstate={published},
  tppubtype={inproceedings}
}

@inproceedings{atienza2021vitstr,
  title={Vision Transformer for Fast and Efficient Scene Text Recognition},
  author={Atienza, Rowel},
  booktitle = {International Conference on Document Analysis and Recognition (ICDAR)},
  year={2021},
  pubstate={published},
  tppubtype={inproceedings}
}
```

## License
Copyright (c) 2019-present NAVER Corp.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

