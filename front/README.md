# Streamlit

작성할 레이아웃 및 기능 : https://docs.google.com/presentation/d/1xEy1XZFwnbeZsMKxkZWbMBLhRQTbyqs-NE2k-w49LJs/edit

## 환경 설정

- 가상환경 이름 : OCR
```python
conda create -n OCR
conda activate OCR
pip install -r requirements.txt
```

## Streamlit 실행
```python
streamlit run app.py
```

## Aistages에서 Streamlit 실행
```python
nohup run .py —server.port=6006 —server.runOnSave=true
```
