# Streamlit

작성할 레이아웃 및 기능 : https://docs.google.com/presentation/d/1xEy1XZFwnbeZsMKxkZWbMBLhRQTbyqs-NE2k-w49LJs/edit

## 환경 설정

- 가상환경 이름 : OCR
```python
conda create -n OCR
conda activate OCR
pip install -r requirements.txt
```

## Streamlit, FastAPI 실행
리눅스
```
make -j 2 run_app
```

윈도우 
```
# FastAPI 백그라운드 실행
start /b python -m app

# Streamlit 포그라운드 실행
streamlit run app/frontend.py
```
