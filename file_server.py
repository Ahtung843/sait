from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)
# Устанавливаем максимальный размер загружаемого файла (например, 2 ГБ)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 * 1024

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return "Сервер файлообменника работает. Ожидание загрузок по адресу /upload"

@app.route('/upload', methods=['POST'])
def upload_file():
    # Проверяем, был ли файл отправлен в запросе
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Нет части 'file' в запросе"}), 400

    file = request.files['file']

    # Если пользователь не выбрал файл, браузер может отправить пустую часть
    if file.filename == '':
        return jsonify({"status": "error", "message": "Нет выбранного файла"}), 400

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        try:
            file.save(filename)
            print(f"Файл успешно сохранен: {filename}")
            return jsonify({"status": "success", "message": f"Файл {file.filename} успешно загружен"}), 200
        except Exception as e:
            print(f"Ошибка сохранения файла: {e}")
            return jsonify({"status": "error", "message": f"Ошибка сохранения файла: {str(e)}"}), 500

if __name__ == '__main__':
    # Запускаем сервер на http://127.0.0.1:5000
    app.run(host='127.0.0.1', port=5000, debug=False)