# SPEC for app.py

## method

### display

GUI Application을 실행한다.

### go_to_result

결과 화면으로 전환한다. (촬영 결과 확인 및 이메일 전송 가능)

### go_to_main

초기 화면으로 전환한다.

### set_result_image

촬영 결과가 저장된 경로를 임시로 저장한다.

### new_picture

카메라 미리보기를 활성화 시킨다.

### take_picture

사진을 촬영한다.

### send_email

이메일을 전송한다.

> 이메일 전송시에 상당한 시간 지연이 있기 때문에 이메일을 전송하는 프로세스를 별도로 생성하여 처리한다.

# SPEC for camera.py

## method

### new_picture

카메라 미리보기를 활성화 시킨다.

### take_picture

타이머(3초) 동작과 함께 overlay 이미지를 카메라 미리보기에 띄워준다.

타이머가 끝나면 사진 촬영후 이미지 편집 작업을 수행한다. 이 때, 빛 센서를 통해 조도 값을 읽어온다.

### send_email

이메일을 전송한다.

# SPEC for image_processing.py

## functions

### insert_datetime

즉석사진처럼 사진에 테두리를 만들고, 아래 여백에 해당 사진을 찍은 시간과 날짜를 추가해준다.

```python
def insert_datetime(img_path):
    ...
```

- parameter
    - `img_path`: image path

### insert_icon

`light`값에 따라 이미지 하단에 해 혹은 달 아이콘을 넣어준다.

```python
def insert_icon(img_path, light):
    ...
```

- parameter
    - `img_path`: image path
    - `light`: data from light sensor

### send_email

이메일을 전송한다.

이 때, 이메일 발신자 계정은 Gmail 계정으로 되어있어야 한다.

비밀번호는 최소한의 보안을 위해 환경변수로 가져오기 때문에 다음의 명령을 입력해서 설정해줘야 한다.

```bash
$ export GMAIL_PASS=password123!@#
```

```python
def send_email(img_path, from_email, to_email):
    ...
```

- parameter
    - `img_path`: image path
    - `from_email`: sender email address
    - `to_email`: receiver email address
