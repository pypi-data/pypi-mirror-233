![Language](https://img.shields.io/badge/English-brigthgreen)

# Motion Detector

![PyPI](https://img.shields.io/pypi/v/motion-detector-g4)
![PyPI - License](https://img.shields.io/pypi/l/motion-detector-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/motion-detector-g4)

Python module for comparing two frames from a video for motion.

***

## Installation

### Package Installation from PyPi

```bash
$ pip install motion-detector-g4
```

### Package Installation from Source Code

The source code is available on [GitHub](https://github.com/Genzo4/motion_detector).  
Download and install the package:

```bash
$ git clone https://github.com/Genzo4/motion_detector
$ cd motion_detector
$ pip install -r requirements.txt
$ pip install .
```

***

## Basic usage

Import:
```python
from motion_detector_g4 import MotionDetector
```

Create an instance of the motion detector. You can specify additional options:
- min_area - minimum tracked change size (blob size).
  Default value: 4000.
- max_area - maximum tracked change size (blob size).
  Default value: 150000.
- noise_size - the maximum size of the removed noise.
  Default value: 10.
- debug - debug mode. If it is enabled, intermediate frames are created, 
  showing the process of processing.
  Default value: False.

```python
md = MotionDetector(min_area=4000, max_area=150000, noise_size=10, debug=False)
```

The module uses the following algorithm:
1. The first frame is being processed (method apply_first_frame).
![Img. 1](https://github.com/Genzo4/motion_detector/raw/main/images/01_frame_1.png "Img. 1 - First frame")
2. The next frame is being processed (method check_motion):
![Img. 2](https://github.com/Genzo4/motion_detector/raw/main/images/01_frame_2.png "Img. 2 - Next frame")
   - the first frame is subtracted from this frame using the module BackgroundSubtractorMOG2
     from the library OpenCV. If debug mode is enabled, then a file is created with an additional 
     extension "mask" with the result of the module.  
     ![Img. 3](https://github.com/Genzo4/motion_detector/raw/main/images/01_frame_2.mask.png "Img. 3 - Removed the background")
   - remove noise using the morphologyEx module from the OpenCV library. This process 
     configured using the noise_size parameter. If debug mode is enabled, then 
     a file is created with the additional extension "clear" with the result of the module's operation.
     ![Img. 4](https://github.com/Genzo4/motion_detector/raw/main/images/01_frame_2.clear.png "Img. 4 - Remove noise")
   - looking for areas of motion (blobs) larger than min_area but smaller than max_area. If debug mode is enabled, then 
     files are created with the extension "blobs" and "blobs2" with the result of the module's operation 
     (found areas are circled in red).
     ![Img. 5](https://github.com/Genzo4/motion_detector/raw/main/images/01_frame_2.blobs.png "Img. 5 - Found areas of interest")
     ![Img. 6](https://github.com/Genzo4/motion_detector/raw/main/images/01_frame_2.blobs2.png "Img. 6 - Found areas of interest")

See the example.py file for an example of usage.

***

![Language](https://img.shields.io/badge/Русский-brigthgreen)

# Motion Detector

![PyPI](https://img.shields.io/pypi/v/motion-detector-g4)
![PyPI - License](https://img.shields.io/pypi/l/motion-detector-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/motion-detector-g4)

Python модуль для сравнения двух кадров из видеозаписи на предмет наличия движения в них.

***

## Установка

### Установка пакета с PyPi

```bash
$ pip install motion-detector-g4
```

### Установка пакета из исходного кода

Исходный код размещается на [GitHub](https://github.com/Genzo4/motion_detector).  
Скачайте его и установите пакет:

```bash
$ git clone https://github.com/Genzo4/motion_detector
$ cd motion_detector
$ pip install -r requirements.txt
$ pip install .
```

***

## Использование

Подключаем:
```python
from motion_detector_g4 import MotionDetector
```

Создаём экземпляр детектора движения. Можно указать дополнительные параметры:
- min_area - минимальный размер отслеживаемого изменения (размера blob'а).
  Значение по умолчанию: 4000.
- max_area - максимальный размер отслеживаемого изменения (размера blob'а).
  Значение по умолчанию: 150000.
- noise_size - максимальный размер удаляемого "шума".
  Значение по умолчанию: 10.
- debug - режим отладки. Если его включить, то создаются промежуточные кадры,
  показывающие процесс обработки.
  Значение по умолчанию: False.

```python
md = MotionDetector(min_area=4000, max_area=150000, noise_size=10, debug=False)
```

В модуле используется следующий алгоритм:
1. Подаётся на обработку первый кадр (метод apply_first_frame).
![Рис. 1](https://github.com/Genzo4/motion_detector/raw/main/images/01_frame_1.png "Рис. 1 - Первый кадр")
2. Подаётся на обработку следующий кадр (метод check_motion):
![Рис. 2](https://github.com/Genzo4/motion_detector/raw/main/images/01_frame_2.png "Рис. 2 - Следующий кадр")
   - из этого кадра "вычитается" первый кадр с помощью модуля BackgroundSubtractorMOG2
     из библиотеки OpenCV. Если включён режим отладки, то создаётся файл с добавочным
     расширением "mask" с результатом работы модуля.  
     ![Рис. 3](https://github.com/Genzo4/motion_detector/raw/main/images/01_frame_2.mask.png "Рис. 3 - Убрали фон")
   - удаляем "шум" с помощью модуля morphologyEx из библиотеки OpenCV. Данный процесс
     настраивается с помощью параметра noise_size. Если включён режим отладки, то
     создаётся файл с добавочным расширением "clear" с результатом работы модуля.
     ![Рис. 4](https://github.com/Genzo4/motion_detector/raw/main/images/01_frame_2.clear.png "Рис. 4 - Очистили от шума")
   - ищем области движения (blob'ы) размером больше min_area, но меньше max_area. Если включён режим отладки, то
     создаются файлы с добавочным расширением "blobs" и "blobs2" с результатом работы модуля 
     (найденные области обводятся красными кругами).
     ![Рис. 5](https://github.com/Genzo4/motion_detector/raw/main/images/01_frame_2.blobs.png "Рис. 5 - Нашли интересующие области движения")
     ![Рис. 6](https://github.com/Genzo4/motion_detector/raw/main/images/01_frame_2.blobs2.png "Рис. 6 - Нашли интересующие области движения")

Пример использования см. в файле example.py
