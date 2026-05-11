# ASCII Art Converter

Инструмент командной строки для преобразования изображений в ASCII-арт на Python.

## Возможности

- Загрузка изображений форматов JPG, PNG, BMP, WEBP и других
- Преобразование в оттенки серого с настраиваемым набором символов
- Настройка ширины результата в символах
- Сохранение результата в текстовый файл
- **Цветной вывод** с использованием ANSI escape-кодов
- Инвертирование яркости для светлого фона терминала
- Четыре встроенных набора символов на выбор

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
├── main.py          — CLI интерфейс (argparse)
├── converter.py     — логика преобразования
├── requirements.txt — зависимости (Pillow)
├── tests/
│   └── test_converter.py — функциональные тесты
├── examples/        — примеры изображений и результатов
├── LICENSE          — MIT лицензия
└── README.md        — документация
```

## Зависимости

- [Pillow](https://pillow.readthedocs.io/) >= 10.0.0 — работа с изображениями

## Лицензия

MIT — см. файл [LICENSE](LICENSE).
