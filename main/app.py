from flask import Flask, render_template

app = Flask(__name__)

FLASK_ENV = "production"
SECRET_KEY = "b207674a1396dc9ed49df9e3e9614a28"
PYTHON_VERSION = "3.13"
PORT = None


@app.route('/')
def home():
    # Отображаем шаблон index.html
    return render_template('index.html')

@app.route('/kartochka')
def kartochka():
    return render_template('kartochka.html')

