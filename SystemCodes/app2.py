import subprocess
import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from images_module.images_checker import *
import shutil

app = Flask(__name__)

DOWNLOAD_FOLDER = "download_folder/"
UPLOAD_FOLDER = "upload_folder/"
UIPATH_FOLDER = "C:/Users/User/PycharmProjects/ISA-IPA-2021-11-17-IS03FT-GRP1-IntelligentMaliciousContentChecker_I-MCC/SystemCodes/UIPath/StaticAnalysis/"
BINARY_ANALYSIS_FOLDER = UIPATH_FOLDER + "malware_beware/"
URL_VT_RESULT = UIPATH_FOLDER + "virustotal_result/"
BINARY_RESULT =UIPATH_FOLDER + "resultfile/"
ROBOT_EXE = "C:/Users/User/AppData/Local/Programs/UiPath/Studio/UiRobot.exe"

@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('upload.html')

@app.route('/url', methods=['GET', 'POST'])
def url():
    url = request.form['say']
    arguments = "{'queryString':'" + url + "'}"
    xamlFile = UIPATH_FOLDER + "QueryVirustotalURL.xaml"
    subprocess.run(ROBOT_EXE + " execute --file '" + xamlFile + "' --input " + arguments, shell=True)
    createzip(URL_VT_RESULT, DOWNLOAD_FOLDER + "urlresult.zip")
    return render_template('download.html', content='urlresult.zip')

@app.route('/images', methods=['GET', 'POST'])
def images():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        to_foldername = UPLOAD_FOLDER + filename.replace(".zip","")
        unzip(UPLOAD_FOLDER+filename, to_foldername)
        folder_detection(to_foldername)
        createzip(to_foldername, DOWNLOAD_FOLDER + "imagesresult.zip")
    return render_template('download.html', content='imagesresult.zip')


@app.route('/zipfile', methods=['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
    shutil.copy(UPLOAD_FOLDER + filename, BINARY_ANALYSIS_FOLDER)
    xamlFile = UIPATH_FOLDER + "MainStaticA.xaml"
    print(ROBOT_EXE + " execute --file '" + xamlFile)
    subprocess.run(ROBOT_EXE + " execute --file '" + xamlFile, shell=True)
    createzip(BINARY_RESULT, DOWNLOAD_FOLDER + "binaryresult.zip")
    shutil.rmtree(BINARY_RESULT)
    os.mkdir(BINARY_RESULT)
    return render_template('download.html', content='binaryresult.zip')


@app.route('/downloads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(DOWNLOAD_FOLDER, DOWNLOAD_FOLDER, filename=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
