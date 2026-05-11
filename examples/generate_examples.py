"""
Скрипт для генерации демонстрационных примеров ASCII-арта.
Создаёт тестовые изображения и конвертирует их.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageDraw, ImageFont

from converter import CHAR_SETS, image_to_ascii, save_to_file


def create_gradient_image(width: int = 300, height: int = 200) -> Image.Image:
    """Создаёт изображение с горизонтальным градиентом."""
    img = Image.new("RGB", (width, height))
    for x in range(width):
        shade = int(x / width * 255)
        for y in range(height):
            img.putpixel((x, y), (shade, shade, shade))
    return img


def create_circle_image(size: int = 200) -> Image.Image:
    """Создаёт изображение с кругом на белом фоне."""
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)
    margin = size // 8
    draw.ellipse([margin, margin, size - margin, size - margin], fill="black")
    return img


def create_checkerboard(size: int = 200, squares: int = 8) -> Image.Image:
    """Создаёт шахматный узор."""
    img = Image.new("RGB", (size, size))
    sq = size // squares
    for row in range(squares):
        for col in range(squares):
            color = "white" if (row + col) % 2 == 0 else "black"
            x0, y0 = col * sq, row * sq
            for x in range(x0, min(x0 + sq, size)):
                for y in range(y0, min(y0 + sq, size)):
                    img.putpixel((x, y), (255, 255, 255) if color == "white" else (0, 0, 0))
    return img


def main():
    examples_dir = os.path.dirname(os.path.abspath(__file__))

    print("Генерация примеров ASCII-арта...")

    # Градиент
    gradient = create_gradient_image()
    gradient_path = os.path.join(examples_dir, "gradient.png")
    gradient.save(gradient_path)
    for charset_name, chars in CHAR_SETS.items():
        art = image_to_ascii(gradient, width=60, chars=chars)
        out_path = os.path.join(examples_dir, f"gradient_{charset_name}.txt")
        save_to_file(art, out_path)
        print(f"  Сохранено: {os.path.basename(out_path)}")

    # Круг
    circle = create_circle_image()
    circle_path = os.path.join(examples_dir, "circle.png")
    circle.save(circle_path)
    art = image_to_ascii(circle, width=60)
    save_to_file(art, os.path.join(examples_dir, "circle_ascii.txt"))
    print("  Сохранено: circle_ascii.txt")

    # Шахматный узор
    checker = create_checkerboard()
    checker_path = os.path.join(examples_dir, "checkerboard.png")
    checker.save(checker_path)
    art = image_to_ascii(checker, width=60)
    save_to_file(art, os.path.join(examples_dir, "checkerboard_ascii.txt"))
    print("  Сохранено: checkerboard_ascii.txt")

    print("\nВсе примеры сгенерированы.")


if __name__ == "__main__":
    main()
