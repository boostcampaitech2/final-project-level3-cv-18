## 1. Position in System

![시스템구조도_백엔드](https://user-images.githubusercontent.com/87659486/147174751-7c24df91-459c-481a-a6cd-234fa181416b.jpg)

![백엔드](https://user-images.githubusercontent.com/87659486/147174681-8c181349-1b42-4422-803b-2d384716f564.jpg)

## 2. Implementation

1. FastAPI 를 이용하여 구현
2. Model cashing
   * 기존 방식의 경우, 요청 1번에 모델 로딩 1번이 일어나 latency 가 아주 길었음.
   * 모델 로딩은 서비스가 처음 제공될 때만 발생하고 그 이후로는 모델이 메모리에 남게 만들어 latency 를 약 3초 가량 줄임.

## 3. For our work

* use port 8501 of backend server.

```bash
$ python back.py &
```
