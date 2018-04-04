from flask import Flask, render_template, request
from diminutivesFinder import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def result():
    diminutives = findDiminutives(request.form['text'])
    return render_template('result.html', diminutives = diminutives)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)
