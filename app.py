"""
Веб-интерфейс для ASCII Art Converter.
Запуск: python app.py
"""

import io
import os

from flask import Flask, render_template, request, send_file

from converter import CHAR_SETS, get_char_set, image_to_ascii, load_image

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 МБ

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "webp", "gif"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", charsets=list(CHAR_SETS.keys()))


@app.route("/convert", methods=["POST"])
def convert():
    file = request.files.get("image")
    if not file or file.filename == "":
        return render_template("index.html", charsets=list(CHAR_SETS.keys()), error="Выберите файл изображения.")

    if not allowed_file(file.filename):
        return render_template(
            "index.html",
            charsets=list(CHAR_SETS.keys()),
            error=f"Неподдерживаемый формат. Разрешены: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    try:
        width = int(request.form.get("width", 80))
        width = max(10, min(500, width))
    except ValueError:
        width = 80

    charset_name = request.form.get("charset", "standard")
    invert = request.form.get("invert") == "on"

    try:
        img_bytes = io.BytesIO(file.read())
        img_bytes.name = file.filename
        from PIL import Image
        img = Image.open(img_bytes)
        img.load()
    except Exception:
        return render_template(
            "index.html",
            charsets=list(CHAR_SETS.keys()),
            error="Не удалось открыть изображение. Убедитесь, что файл не повреждён.",
        )

    try:
        chars = get_char_set(charset_name)
        ascii_art = image_to_ascii(img, width=width, chars=chars, invert=invert)
    except Exception as e:
        return render_template("index.html", charsets=list(CHAR_SETS.keys()), error=f"Ошибка конвертации: {e}")

    line_count = ascii_art.count("\n") + 1
    return render_template(
        "index.html",
        charsets=list(CHAR_SETS.keys()),
        ascii_art=ascii_art,
        width=width,
        charset=charset_name,
        invert=invert,
        filename=file.filename,
        line_count=line_count,
        char_count=len(ascii_art.replace("\n", "")),
    )


@app.route("/download", methods=["POST"])
def download():
    ascii_art = request.form.get("ascii_art", "")
    filename = request.form.get("filename", "image")
    stem = os.path.splitext(filename)[0]
    buf = io.BytesIO(ascii_art.encode("utf-8"))
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name=f"{stem}_ascii.txt", mimetype="text/plain; charset=utf-8")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
