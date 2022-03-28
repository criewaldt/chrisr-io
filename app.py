from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import requests

from utils import opendata
from settings.settings import RECAPTCHA_SITE, RECAPTCHA_SECRET 

is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    recaptcha_site = os.environ.get('RECAPTCHA_SITE')
    recaptcha_secret = os.environ.get('RECAPTCHA_SECRET')
else:
    recaptcha_site = RECAPTCHA_SITE
    recaptcha_secret = RECAPTCHA_SECRET


def get_files():
    file_list = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(dir_path, "static")
    output_path = os.path.join(output_path, "output")
    for file in os.listdir(output_path):
        if file.endswith(".xls"):
            file_list.append(file)
    return file_list


def verifyRecaptcha(token):
    url = "https://www.google.com/recaptcha/api/siteverify?secret={}&response={}".format(recaptcha_secret, token)
    r = requests.get(url)
    return r.json()




app = Flask(__name__)

@app.route("/")
def main():
    return render_template('main.html')
    
@app.route("/index")
def index():
    return render_template('index.html')
    
@app.route("/docs")
def bin_docs():
    docs = get_files()
    return render_template('bin_docs.html', docs=docs)

@app.route('/bin/', methods=['POST'])
def bin_num():
    #recaptcha check
    recaptcha_token = request.form['g-recaptcha-response']
    weGood = verifyRecaptcha(recaptcha_token)
    if weGood['success'] == False:
        print('we not good - check recaptcha')
        print(weGood)
        return redirect(url_for('index'))
    return redirect(url_for('main'))

    """
    # something
    bin_number = request.form['bin']
    if len(bin_number) == 7 and bin_number.isdigit() ==  True:
    
        print("..Getting data for BIN# {}".format(bin_number))
    
        j = opendata.GetBin(bin_number)
        s = opendata.Spreadsheet(bin_number)
        for job in j.now_jobs:
            s.Job(job)
        for job in j.bis_jobs:
            s.Job(job)
        s.DOBViolations(j.violations)
        s.ECBViolations(j.ecb)
        
        docs = get_files()
        return render_template('bin_docs.html', docs=docs)
     
    else:
    
        print("BIN incorrect format")
        return redirect(url_for('main'))
    """    

    

@app.route('/static/output/<path:path>')
def send_report(path):
    return send_from_directory('static/output', path)























