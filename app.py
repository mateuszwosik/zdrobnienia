from flask import Flask, render_template, request
from diminutivesFinder import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def result():
    result = findDiminutives(request.form['text'])
    diminutives = result["diminutives"]
    stats = result["stats"]
    words = getOnlyDiminutives(diminutives)
    return render_template('result.html', diminutives = diminutives, text = request.form['text'], stats = stats, words = words)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/report')
def report():
    return render_template('report.html')

if __name__ == '__main__':
    #app.run()
    app.run(debug=True)
