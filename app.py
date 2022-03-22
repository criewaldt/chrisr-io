from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os


from utils import opendata

def get_files():
    file_list = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(dir_path, "output")
    for file in os.listdir(output_path):
        if file.endswith(".xls"):
            file_list.append(file)
    return file_list

app = Flask(__name__,
            static_url_path='', 
            static_folder='/output')

@app.route("/")
def main():
    return render_template('main.html')
    
@app.route("/docs")
def bin_docs():
    docs = get_files()
    return render_template('bin_docs.html', docs=docs)

@app.route('/bin/', methods=['POST'])
def bin_num():
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
        print("bin incorrect format")
        return redirect(url_for('main'))
        

    

@app.route('/output/<path:path>')
def send_report(path):
    return send_from_directory('output', path)




















