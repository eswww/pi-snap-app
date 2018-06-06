# SPEC for image_processing.py

## functions

### insert_datetime

사진에 폴라로이드처럼 테두리를 만들고, 아래 여백에 해당 사진을 찍은 시간을 넣어준다.

```python
def insert_datetime(image_path):
    ...
    return out
```

- parameter
    - `image_path`: image path
- return value
    - `out`: image object

### insert_icon

`light`값에 따라 이미지 하단에 해 혹은 달 아이콘을 넣어준다.

```python
def insert_icon(img, light):
    ...
    return img
```

- parameter
    - `img`: image object
    - `light`: data from light sensor
- return value
    - `out`: image object