CUDA_VISIBLE_DEVICES=0 python3 train.py --train_data lmdb_result/#v2_nospace/ --valid_data lmdb_result/#v3_valid_nospace/ --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn --batch_size 64 --num_iter 1000 --input_channel 1 --valInterval 50 --saved_model ./pretrained/TPS-ResNet-BiLSTM-Attn-case-sensitive.pth --sensitive






