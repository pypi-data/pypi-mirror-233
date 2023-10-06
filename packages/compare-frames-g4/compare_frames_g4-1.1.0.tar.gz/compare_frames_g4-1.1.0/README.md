![Language](https://img.shields.io/badge/English-brigthgreen)

# Compare frames

![PyPI](https://img.shields.io/pypi/v/compare-frames-g4)
![PyPI - License](https://img.shields.io/pypi/l/compare-frames-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/compare-frames-g4)


Compare 2 frames

***

## Installation

### Package Installation from PyPi

```bash
$ pip install compare-frames-g4
```

### Package Installation from Source Code

The source code is available on [GitHub](https://github.com/Genzo4/compare_frames).  
Download and install the package:

```bash
$ git clone https://github.com/Genzo4/compare_frames
$ cd compare_frames
$ pip install -r requirements.txt
$ pip install .
```

***

## Usage

- From files

```python
from compare_frames_g4 import compare_frames

is_equal = compare_frames('path_to_frame_1', 'path_to_frame_2')
```

- From frames (numpy.ndarray)

```python
from compare_frames_g4 import compare_frames
import cv2

frame_1 = cv2.imread('path_to_frame_1')
frame_2 = cv2.imread('path_to_frame_2')

is_equal = compare_frames(frame_1, frame_2)
```

- Mix

```python
from compare_frames_g4 import compare_frames
import cv2

frame_1 = cv2.imread('path_to_frame_1')

is_equal = compare_frames(frame_1, 'path_to_frame_2')
```

```python
from compare_frames_g4 import compare_frames
import cv2

frame_2 = cv2.imread('path_to_frame_2')

is_equal = compare_frames('path_to_frame_2', frame_2)
```

***

[Changelog](https://github.com/Genzo4/compare_frames/blob/main/CHANGELOG.md)

***

![Language](https://img.shields.io/badge/Русский-brigthgreen)

# Compare frames

![PyPI](https://img.shields.io/pypi/v/compare-frames-g4)
![PyPI - License](https://img.shields.io/pypi/l/compare-frames-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/compare-frames-g4)

Сравнение двух кадров (изображений).

***

## Установка

### Установка пакета с PyPi

```bash
$ pip install compare-frames-g4
```

### Установка пакета из исходного кода

Исходный код размещается на [GitHub](https://github.com/Genzo4/compare_frames).  
Скачайте его и установите пакет:

```bash
$ git clone https://github.com/Genzo4/compare_frames
$ cd compare_frames
$ pip install -r requirements.txt
$ pip install .
```

***

## Использование

- Берём кадры из файлов 

```python
from compare_frames_g4 import compare_frames

is_equal = compare_frames('path_to_frame_1', 'path_to_frame_2')
```

- Используем "готовые" кадры (numpy.ndarray). Например, из cv2.imread

```python
from compare_frames_g4 import compare_frames
import cv2

frame_1 = cv2.imread('path_to_frame_1')
frame_2 = cv2.imread('path_to_frame_2')

is_equal = compare_frames(frame_1, frame_2)
```

- Смешанный режим

```python
from compare_frames_g4 import compare_frames
import cv2

frame_1 = cv2.imread('path_to_frame_1')

is_equal = compare_frames(frame_1, 'path_to_frame_2')
```

```python
from compare_frames_g4 import compare_frames
import cv2

frame_2 = cv2.imread('path_to_frame_2')

is_equal = compare_frames('path_to_frame_2', frame_2)
```

***

[Changelog](https://github.com/Genzo4/compare_frames/blob/main/CHANGELOG.md)
