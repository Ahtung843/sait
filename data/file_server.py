from flask import Flask, request, jsonify
from mega import Mega
import os
import io

app = Flask(__name__)

def mega_client():
    email = os.environ.get("MEGA_EMAIL")
    password = os.environ.get("MEGA_PASSWORD")

    if not email or not password:
        raise RuntimeError("Не указаны переменные MEGA_EMAIL или MEGA_PASSWORD")

    mega = Mega()
    return mega.login(email, password)

@app.route("/")
def index():
    return "Файлообменник работает (Render + MEGA). Загрузка доступна по POST /upload"

@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return jsonify({"status": "error", "message": "Файл не найден"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"status": "error", "message": "Имя файла пустое"}), 400

    try:
        m = mega_client()

        # сохраняем временно в память
        content = file.read()
        file_stream = io.BytesIO(content)

        uploaded_file = m.upload(file_stream, file.filename)

        public_link = m.get_link(uploaded_file)

        return jsonify({
            "status": "success",
            "file_name": file.filename,
            "mega_public_link": public_link
        }), 200

    except Exception as e:
        print("Ошибка:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
