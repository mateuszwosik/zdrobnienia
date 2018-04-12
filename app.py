from flask import Flask, render_template, request
from flask_mail import Mail, Message
from diminutivesFinder import *

app = Flask(__name__)
mail = Mail(app)

app.config.update(
    #EMAIL SETTINGS
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'wyszukiwarkazdrobnien@gmail.com',
    MAIL_PASSWORD = '')

mail = Mail(app)

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

@app.route('/report', methods=['GET','POST'])
def report():
    if request.method == "POST":
        #sending mail
        msg = Message('REPORT - zgłoszono słowo',
                      sender = 'wyszukiwarkazdrobnien@gmail.com',
                      recipients = ['wyszukiwarkazdrobnien@gmail.com'])
        msg.body = "SŁOWO: " + request.form['word'] + " \r\nKOMENTARZ: " + request.form['comment']
        mail.send(msg)        
    return render_template('report.html')

if __name__ == '__main__':
    #app.run()
    #app.run(debug=True)
    app.run()
