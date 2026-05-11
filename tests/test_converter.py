"""
Функциональные тесты для модуля converter.py
"""

import os
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from converter import (
    CHAR_SETS,
    get_char_set,
    image_to_ascii,
    image_to_ascii_color,
    load_image,
    pixel_to_char,
    resize_image,
    save_to_file,
    to_grayscale,
)


def make_test_image(width: int = 100, height: int = 80, color: tuple = (128, 64, 32)) -> Image.Image:
    """Создаёт тестовое изображение заданного размера и цвета."""
    img = Image.new("RGB", (width, height), color)
    return img


class TestPixelToChar(unittest.TestCase):
    def test_darkest_pixel(self):
        chars = "@%#*+=-:. "
        self.assertEqual(pixel_to_char(0, chars), "@")

    def test_brightest_pixel(self):
        chars = "@%#*+=-:. "
        self.assertEqual(pixel_to_char(255, chars), " ")

    def test_midpoint(self):
        chars = "AB"
        result = pixel_to_char(128, chars)
        self.assertIn(result, "AB")

    def test_single_char(self):
        self.assertEqual(pixel_to_char(0, "X"), "X")
        self.assertEqual(pixel_to_char(255, "X"), "X")


class TestResizeImage(unittest.TestCase):
    def test_width_is_respected(self):
        img = make_test_image(200, 100)
        resized = resize_image(img, 50)
        self.assertEqual(resized.width, 50)

    def test_height_scales_with_aspect_ratio(self):
        img = make_test_image(200, 200)
        resized = resize_image(img, 100)
        # Высота должна быть ~45% от ширины (квадратное изображение)
        expected_height = int(100 * 0.45)
        self.assertEqual(resized.height, expected_height)

    def test_small_image(self):
        img = make_test_image(10, 10)
        resized = resize_image(img, 20)
        self.assertEqual(resized.width, 20)


class TestToGrayscale(unittest.TestCase):
    def test_rgb_to_grayscale(self):
        img = make_test_image()
        gray = to_grayscale(img)
        self.assertEqual(gray.mode, "L")

    def test_already_grayscale(self):
        img = Image.new("L", (50, 50), 128)
        gray = to_grayscale(img)
        self.assertEqual(gray.mode, "L")

    def test_rgba_to_grayscale(self):
        img = Image.new("RGBA", (50, 50), (255, 0, 0, 128))
        gray = to_grayscale(img)
        self.assertEqual(gray.mode, "L")


class TestImageToAscii(unittest.TestCase):
    def test_output_is_string(self):
        img = make_test_image()
        result = image_to_ascii(img, width=20)
        self.assertIsInstance(result, str)

    def test_width_in_chars(self):
        img = make_test_image()
        width = 40
        result = image_to_ascii(img, width=width)
        first_line = result.split("\n")[0]
        self.assertEqual(len(first_line), width)

    def test_line_count(self):
        img = make_test_image(100, 100)
        result = image_to_ascii(img, width=50)
        lines = result.split("\n")
        expected_height = int(50 * 0.45)
        self.assertEqual(len(lines), expected_height)

    def test_invert_changes_output(self):
        img = make_test_image(50, 50, color=(0, 0, 0))
        normal = image_to_ascii(img, width=20, invert=False)
        inverted = image_to_ascii(img, width=20, invert=True)
        self.assertNotEqual(normal, inverted)

    def test_custom_charset(self):
        img = make_test_image()
        chars = "AB"
        result = image_to_ascii(img, width=20, chars=chars)
        for char in result:
            if char != "\n":
                self.assertIn(char, chars)

    def test_different_charsets(self):
        img = make_test_image()
        for name, chars in CHAR_SETS.items():
            result = image_to_ascii(img, width=20, chars=chars)
            self.assertIsInstance(result, str, f"Сбой для набора символов: {name}")


class TestImageToAsciiColor(unittest.TestCase):
    def test_contains_ansi_codes(self):
        img = make_test_image()
        result = image_to_ascii_color(img, width=20)
        self.assertIn("\033[", result)
        self.assertIn("\033[0m", result)

    def test_output_is_string(self):
        img = make_test_image()
        result = image_to_ascii_color(img, width=20)
        self.assertIsInstance(result, str)


class TestLoadImage(unittest.TestCase):
    def test_load_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            load_image("nonexistent_file_xyz.jpg")

    def test_load_valid_image(self):
        img = make_test_image()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            img.save(tmp_path)
            loaded = load_image(tmp_path)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.width, 100)
            loaded.close()
        finally:
            os.unlink(tmp_path)

    def test_load_invalid_file(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False, mode="w") as tmp:
            tmp.write("это не изображение")
            tmp_path = tmp.name
        try:
            with self.assertRaises(ValueError):
                load_image(tmp_path)
        finally:
            os.unlink(tmp_path)


class TestSaveToFile(unittest.TestCase):
    def test_save_and_read_back(self):
        content = "ASCII art\nline 2\nline 3"
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            save_to_file(content, tmp_path)
            with open(tmp_path, "r", encoding="utf-8") as f:
                read_back = f.read()
            self.assertEqual(content, read_back)
        finally:
            os.unlink(tmp_path)

    def test_unicode_content(self):
        content = "Тест кириллицы: @#%*"
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            save_to_file(content, tmp_path)
            with open(tmp_path, "r", encoding="utf-8") as f:
                read_back = f.read()
            self.assertEqual(content, read_back)
        finally:
            os.unlink(tmp_path)


class TestGetCharSet(unittest.TestCase):
    def test_valid_charsets(self):
        for name in CHAR_SETS:
            chars = get_char_set(name)
            self.assertEqual(chars, CHAR_SETS[name])

    def test_invalid_charset(self):
        with self.assertRaises(ValueError):
            get_char_set("nonexistent_charset")


class TestEndToEnd(unittest.TestCase):
    """Интеграционные тесты полного цикла конвертации."""

    def test_full_pipeline_png(self):
        img = make_test_image(200, 150)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img_path = tmp.name
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            out_path = tmp.name
        try:
            img.save(img_path)
            loaded = load_image(img_path)
            ascii_art = image_to_ascii(loaded, width=60)
            save_to_file(ascii_art, out_path)
            with open(out_path, "r", encoding="utf-8") as f:
                result = f.read()
            self.assertEqual(ascii_art, result)
        finally:
            os.unlink(img_path)
            os.unlink(out_path)

    def test_full_pipeline_width_variations(self):
        img = make_test_image(300, 200)
        for width in [20, 50, 80, 120, 200]:
            result = image_to_ascii(img, width=width)
            first_line = result.split("\n")[0]
            self.assertEqual(len(first_line), width, f"Ширина {width} не совпадает")


if __name__ == "__main__":
    unittest.main(verbosity=2)
