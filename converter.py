"""
Модуль преобразования изображений в ASCII-арт.
"""

from PIL import Image


# Наборы символов от тёмного к светлому
CHAR_SETS = {
    "standard": "@%#*+=-:. ",
    "detailed": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    "simple": "@#+-. ",
    "blocks": "█▓▒░ ",
}

DEFAULT_CHARS = CHAR_SETS["standard"]


def load_image(path: str) -> Image.Image:
    """Загружает изображение с диска."""
    try:
        img = Image.open(path)
        return img
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {path}")
    except Exception as e:
        raise ValueError(f"Не удалось открыть изображение: {e}")


def resize_image(img: Image.Image, width: int) -> Image.Image:
    """Изменяет размер изображения с сохранением пропорций."""
    original_width, original_height = img.size
    # Символы в консоли выше, чем шире — компенсируем коэффициентом 0.45
    aspect_ratio = original_height / original_width * 0.45
    height = int(width * aspect_ratio)
    return img.resize((width, height))


def to_grayscale(img: Image.Image) -> Image.Image:
    """Конвертирует изображение в оттенки серого."""
    return img.convert("L")


def pixel_to_char(brightness: int, chars: str) -> str:
    """Преобразует значение яркости (0-255) в ASCII-символ."""
    index = int(brightness / 255 * (len(chars) - 1))
    return chars[index]


def image_to_ascii(
    img: Image.Image,
    width: int = 80,
    chars: str = DEFAULT_CHARS,
    invert: bool = False,
) -> str:
    """
    Преобразует изображение в ASCII-арт.

    Args:
        img: PIL-изображение
        width: ширина результата в символах
        chars: набор символов для отображения яркости
        invert: инвертировать яркость (для светлого фона)

    Returns:
        Строка с ASCII-артом
    """
    img = resize_image(img, width)
    img = to_grayscale(img)

    char_set = chars[::-1] if invert else chars
    lines = []
    for y in range(img.height):
        row = ""
        for x in range(img.width):
            brightness = img.getpixel((x, y))
            row += pixel_to_char(brightness, char_set)
        lines.append(row)

    return "\n".join(lines)


def image_to_ascii_color(img: Image.Image, width: int = 80, chars: str = DEFAULT_CHARS) -> str:
    """
    Преобразует изображение в цветной ASCII-арт (ANSI escape-коды).

    Args:
        img: PIL-изображение
        width: ширина результата в символах
        chars: набор символов для отображения яркости

    Returns:
        Строка с цветным ASCII-артом
    """
    img_resized = resize_image(img, width)
    img_color = img_resized.convert("RGB")
    img_gray = img_resized.convert("L")

    lines = []
    for y in range(img_resized.height):
        row = ""
        for x in range(img_resized.width):
            r, g, b = img_color.getpixel((x, y))
            brightness = img_gray.getpixel((x, y))
            char = pixel_to_char(brightness, chars)
            row += f"\033[38;2;{r};{g};{b}m{char}"
        row += "\033[0m"
        lines.append(row)

    return "\n".join(lines)


def save_to_file(ascii_art: str, output_path: str) -> None:
    """Сохраняет ASCII-арт в текстовый файл."""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ascii_art)
    except IOError as e:
        raise IOError(f"Не удалось сохранить файл: {e}")


def get_char_set(name: str) -> str:
    """Возвращает набор символов по имени."""
    if name not in CHAR_SETS:
        available = ", ".join(CHAR_SETS.keys())
        raise ValueError(f"Набор символов '{name}' не найден. Доступные: {available}")
    return CHAR_SETS[name]
