from flask import Flask, render_template, request, send_from_directory
import os

from opendata import Spreadsheet, GetBin

app = Flask(__name__,
            static_url_path='', 
            static_folder='/output')

@app.route("/")
def main():
    return render_template('bin.html')

@app.route('/bin/', methods=['POST'])
def bin_num():
    # something
    bin_number = request.form['bin']

    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(dir_path, "output")
    docs = os.listdir(output_path)
    
    j = GetBin(bin_num)
    s = Spreadsheet(bin_num, j.address)
    for job in j.now_jobs:
        s.Job(job)
    for job in j.bis_jobs:
        s.Job(job)
    s.DOBViolations(j.violations)
    s.ECBViolations(j.ecb)

    return render_template('bin_docs.html', docs=docs)

@app.route('/output/<path:path>')
def send_report(path):
    return send_from_directory('output', path)

    