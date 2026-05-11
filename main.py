"""
ASCII Art Converter — главный скрипт с CLI интерфейсом.

Использование:
    python main.py input.jpg
    python main.py input.jpg -w 120
    python main.py input.jpg -o output.txt
    python main.py input.jpg -c
    python main.py input.jpg --charset detailed --invert
"""

import argparse
import sys

from converter import (
    CHAR_SETS,
    get_char_set,
    image_to_ascii,
    image_to_ascii_color,
    load_image,
    save_to_file,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ascii-art",
        description="Преобразование изображений в ASCII-арт",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py photo.jpg
  python main.py photo.jpg -w 120
  python main.py photo.jpg -o result.txt
  python main.py photo.jpg -c
  python main.py photo.jpg --charset detailed -w 80 -o art.txt
  python main.py photo.jpg --invert
        """,
    )

    parser.add_argument("image", help="Путь к изображению (JPG, PNG, BMP и др.)")

    parser.add_argument(
        "-w", "--width",
        type=int,
        default=80,
        metavar="N",
        help="Ширина ASCII-арта в символах (по умолчанию: 80)",
    )

    parser.add_argument(
        "-o", "--output",
        metavar="ФАЙЛ",
        help="Путь для сохранения результата в .txt файл",
    )

    parser.add_argument(
        "-c", "--color",
        action="store_true",
        help="Использовать цветной вывод (ANSI escape-коды)",
    )

    parser.add_argument(
        "--charset",
        choices=list(CHAR_SETS.keys()),
        default="standard",
        help="Набор символов для отображения (по умолчанию: standard)",
    )

    parser.add_argument(
        "--invert",
        action="store_true",
        help="Инвертировать яркость (для светлого фона терминала)",
    )

    parser.add_argument(
        "--no-print",
        action="store_true",
        help="Не выводить результат в консоль (только сохранить в файл)",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.width < 10 or args.width > 500:
        print(f"Ошибка: ширина должна быть от 10 до 500 символов (указано: {args.width})", file=sys.stderr)
        return 1

    try:
        print(f"Загружаю изображение: {args.image}", file=sys.stderr)
        img = load_image(args.image)
        print(f"Размер: {img.width}×{img.height} пкс, режим: {img.mode}", file=sys.stderr)
    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1

    try:
        chars = get_char_set(args.charset)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1

    try:
        if args.color:
            ascii_art = image_to_ascii_color(img, width=args.width, chars=chars)
        else:
            ascii_art = image_to_ascii(img, width=args.width, chars=chars, invert=args.invert)
    except Exception as e:
        print(f"Ошибка при конвертации: {e}", file=sys.stderr)
        return 1

    if not args.no_print:
        print(ascii_art)

    if args.output:
        # При сохранении в файл убираем ANSI-коды если был цветной режим
        if args.color:
            plain = image_to_ascii(img, width=args.width, chars=chars, invert=args.invert)
        else:
            plain = ascii_art
        try:
            save_to_file(plain, args.output)
            print(f"\nСохранено в: {args.output}", file=sys.stderr)
        except IOError as e:
            print(f"Ошибка сохранения: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
