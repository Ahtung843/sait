from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    # Отображаем шаблон index.html
    return render_template('index.html')

@app.route('/kartochka')
def kartochka():
    return render_template('kartochka.html')

if __name__ == '__main__':
    app.run(debug=True)