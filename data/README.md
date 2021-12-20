# EDA for data generation

```python
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
```

```python
df = pd.read_csv("STR_C+G_1353.csv")
df.head()
```

![image-20211217105623433](https://user-images.githubusercontent.com/87659486/146477306-a867e516-0c66-44b9-8ea7-60f7524d74a5.png)



```python
collect = df[df['image_type']=='collect'].copy()
collect.head()
```

![image-20211217105706638](https://user-images.githubusercontent.com/87659486/146477342-009709d5-6b15-440e-9704-08f9582c1af1.png)



## image, text, status

```python
collect.groupby(['status']).count()
```

![image-20211217105902578](https://user-images.githubusercontent.com/87659486/146477373-5f01abc8-4463-4d83-8a6b-c97370eea79d.png)



```python
collect.groupby(['letter']).count()
```

![image-20211217105922318](https://user-images.githubusercontent.com/87659486/146477394-911fa5ce-d899-491d-9dde-d46a585636f7.png)



```python
collect.groupby(['environment']).count()
```

![image-20211217105941653](https://user-images.githubusercontent.com/87659486/146477414-b1683095-ad2d-4563-820a-b4f0c8b35bad.png)



```python
collect.groupby(['status', 'letter', 'environment']).count()
```

![image-20211217105957687](https://user-images.githubusercontent.com/87659486/146477441-a3fc916c-5fbd-4e1f-bd3d-ad877446c9db.png)

> 텍스트가 가로쓰기이면서 글자 상태가 깨끗하고 사진이 빛을 충분히 받아 깨끗한 경우의 데이터가 제일 많다.  
>
> 기울어진 텍스트는 그 다음으로 많다.  
>
> 사진이 찍히면서 흔들린 경우, 흐린 글자가 포함된 경우도 꽤 있다.

## Image width and height

### Joint Plot

```python
sns.jointplot(x="image_w", y="image_h", data=collect)
plt.suptitle("image weight, height Joint Plot", y=1.02)
plt.show()
```

![image-20211217110022055](https://user-images.githubusercontent.com/87659486/146477478-750ae1d6-3efd-4fd1-92da-19458954a9a7.png)

### statistics

```python
arr_h = []
arr_w = []
for h, w in zip(collect['image_h'], collect['image_w']):
    arr_h.append(h)
    arr_w.append(w)
    
# 이미지 가로 및 세로 최대 길이, 최소 길이, 평균값, 중앙값, 최빈값
print('이미지 가로, 세로')
print('최대 길이 :',np.max(arr_w), np.max(arr_h))
print('최소 길이 :',np.min(arr_w), np.min(arr_h))
print('평균값 :',np.mean(arr_w), np.mean(arr_h))
print('중앙값 :',np.median(arr_w), np.median(arr_h))
print('최빈값 :',stats.mode(arr_w)[0][0], stats.mode(arr_h)[0][0])
```

| 이미지    | 가로  | 세로   |
| :-------- | :---- | ------ |
| 최대 길이 | 342   | 917    |
| 최소 길이 | 20    | 67     |
| 평균값    | 75.82 | 290.24 |
| 중앙값    | 63.0  | 203.0  |
| 최빈값    | 48    | 134    |



## Length of product number

### KDE Plot

```python
sns.kdeplot(collect['product_no_len'])
plt.show()
```

![image-20211217110337331](https://user-images.githubusercontent.com/87659486/146477504-fa6719c3-9003-4215-b730-c1c32f39918d.png)

### statistics

```python
arr_len = []
for i in collect['product_no']:
    arr_len.append(len(i))
    
# 상품번호 최대 길이, 최소 길이, 평균값, 중앙값, 최빈값
print('상품번호')
print('최대 길이 :',np.max(arr_len))
print('최소 길이 :',np.min(arr_len))
print('평균값 :',np.mean(arr_len))
print('중앙값 :',np.median(arr_len))
print('최빈값 :',mode(arr_len)[0][0])
```

|           | 상품번호 |
| --------- | -------- |
| 최대 길이 | 15       |
| 최소 길이 | 6        |
| 평균값    | 8.44     |
| 중앙값    | 9.0      |
| 최빈값    | 10       |



## Image width, height and length of product number

```python
sns.jointplot(x="image_w", y="product_no_len", data=collect)
plt.suptitle("image weight, product_no_len Joint Plot", y=1.02)
plt.show()
```

![image-20211217110459179](https://user-images.githubusercontent.com/87659486/146477526-2c5d93d5-0f71-4118-b6e2-48fb3e16a589.png)

```python
sns.jointplot(x="image_h", y="product_no_len", data=collect)
plt.suptitle("image height, product_no_len Joint Plot", y=1.02)
plt.show()
```

![image-20211217110517519](https://user-images.githubusercontent.com/87659486/146477598-7c63ecdb-e3b9-4464-80b2-f63c8bdca0c9.png)



## EDA for split Train/Valid/Test datasets.

```python
collect[collect['status']=='Left_Rot']
```

![image-20211217110759969](https://user-images.githubusercontent.com/87659486/146477624-ead5022e-1bf9-48e5-893c-bc3bad0c38ca.png)



```python
collect[collect['status']=='Right_Rot']
```

![image-20211217110813553](https://user-images.githubusercontent.com/87659486/146477662-59a2f213-5834-4cc3-9468-907152b21fa7.png)



```python
collect[collect['status']=='Diagonal'].groupby(['letter']).count()
```

![image-20211217110833442](https://user-images.githubusercontent.com/87659486/146477691-7791921d-70a1-4dea-894e-c8ec88def8c8.png)



```python
collect[collect['status']=='Horizontal']
```

![image-20211217110848476](https://user-images.githubusercontent.com/87659486/146477727-e4972430-e5f9-4d51-88da-f87360914162.png)
