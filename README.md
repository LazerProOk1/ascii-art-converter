# ASCII Art Converter

Превращает изображения в ASCII-арт. Есть консольная утилита и веб-интерфейс на Flask.

## Возможности

- Загрузка изображений форматов JPG, PNG, BMP, WEBP и других
- Преобразование в оттенки серого с настраиваемым набором символов
- Настройка ширины результата в символах
- Сохранение результата в текстовый файл
- **Цветной вывод** с использованием ANSI escape-кодов
- Инвертирование яркости для светлого фона терминала
- Четыре встроенных набора символов на выбор
- Веб-интерфейс на Flask: загрузка картинки прямо из браузера

## Установка

```bash
git clone https://github.com/LazerProOk1/ascii-art-converter.git
cd ascii-art-converter
pip install -r requirements.txt
```

## Использование

### Базовые команды

```bash
# Простое преобразование (ширина 80 символов по умолчанию)
python main.py input.jpg

# Задать ширину 120 символов
python main.py input.jpg -w 120

# Сохранить результат в файл
python main.py input.jpg -o output.txt

# Цветной вывод (ANSI)
python main.py input.jpg -c

# Инвертировать для светлого фона
python main.py input.jpg --invert
```

### Наборы символов

```bash
# standard (по умолчанию): @%#*+=-:. 
python main.py input.jpg --charset standard

# detailed — максимальная детализация
python main.py input.jpg --charset detailed

# simple — минималистичный
python main.py input.jpg --charset simple

# blocks — блочные символы Unicode
python main.py input.jpg --charset blocks
```

### Комбинирование параметров

```bash
# Детальный, 120 символов, сохранить в файл
python main.py input.jpg --charset detailed -w 120 -o art.txt

# Цветной, 100 символов, без вывода в консоль
python main.py input.jpg -c -w 100 --no-print -o result.txt
```

### Все параметры

| Параметр | Короткий | Описание | По умолчанию |
|---|---|---|---|
| `image` | — | Путь к изображению | обязательный |
| `--width` | `-w` | Ширина в символах (10–500) | `80` |
| `--output` | `-o` | Путь для сохранения .txt | — |
| `--color` | `-c` | Цветной вывод (ANSI) | выключено |
| `--charset` | — | Набор символов | `standard` |
| `--invert` | — | Инвертировать яркость | выключено |
| `--no-print` | — | Не выводить в консоль | выключено |

## Веб-интерфейс

Кроме консоли есть страница на Flask: выбираешь картинку (можно перетащить), набор символов, ширину и инверсию. Результат показывается в браузере, копируется в буфер и скачивается в `.txt`.

```bash
pip install -r requirements.txt
python app.py
```

Страница откроется на http://127.0.0.1:5000. Форматы: jpg, jpeg, png, bmp, webp, gif; файл до 10 МБ.

## Примеры вывода

```
@@@@@@@@@@@@%#*+=-:. .:-=+*#%@@@@@@@@@@@@
@@@@@@@@@%#*+=-:. . . .::-=+*#%@@@@@@@@@
@@@@@@@@%#+=-:. . . .:-=+#%@@@@@@@@
@@@@@@@%#*=-:. . . . .::-=+*#%@@@@@@@
@@@@@@%#+=-. . . . . .:-=+#%@@@@@@
```

## Запуск тестов

```bash
# Все тесты
python -m pytest tests/ -v

# Или через unittest
python -m unittest discover tests -v
```

## Структура проекта

```
ascii-art-converter/
├── main.py            — CLI интерфейс (argparse)
├── app.py             — веб-интерфейс на Flask
├── converter.py       — логика преобразования
├── templates/
│   └── index.html     — страница загрузки и результат
├── static/
│   ├── style.css      — оформление
│   └── app.js         — перетаскивание файла, превью, копирование
├── requirements.txt   — зависимости (Pillow, Flask)
├── tests/
│   └── test_converter.py — функциональные тесты
├── examples/          — примеры изображений и результатов
├── LICENSE            — MIT лицензия
└── README.md          — документация
```

## Зависимости

- [Pillow](https://pillow.readthedocs.io/) >= 10.0.0 — работа с изображениями
- [Flask](https://flask.palletsprojects.com/) >= 3.0.0 — веб-интерфейс

## Лицензия

MIT — см. файл [LICENSE](LICENSE).
