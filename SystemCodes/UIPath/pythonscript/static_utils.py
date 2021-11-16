# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 23:14:08 2021

@author: Medy
"""

## extracting zip with password
import zipfile
import os
import shutil

#from fpdf import FPDF


#contain all uploaded zip files to be analysed
MAL_WORK_FOLDER = "malware_beware/"
#contains all unzip files
MAL_UNZIP_FOLDER = 'malware_beware/unzip/'
#resultfolder
RESULT_FOLDER = 'resultfile/'
#contain done analyze zip files
DONE_ANALYZED_FOLDER = "done_analyse/"

passwd = "malware"

def createzip(source_dir, output_filename):
    zip = zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED)
    # pre_len = len(os.path.dirname(source_dir))
    for path, dirnames, filenames in os.walk(source_dir):
        fpath = path.replace(source_dir, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()

    
def unpack_allzipfile():
    unzipfile_name = list()
    try:
        for zipname in os.listdir(MAL_WORK_FOLDER):
            if ".zip" not in zipname or "unzip" in zipname:
                if os.path.isfile(zipname):  
                    os.remove(MAL_WORK_FOLDER+zipname)
                continue
            else:
                unzip_with_password(MAL_WORK_FOLDER + zipname, passwd, MAL_UNZIP_FOLDER)
                os.chmod(MAL_UNZIP_FOLDER, mode=777)
        unzipfile_name = [file for file in os.listdir(MAL_UNZIP_FOLDER)]
    except Exception as e:
        print(e)
    # print(unzipfile_name)
    return unzipfile_name

def unzip_with_password(zipname, password, tofolder):
    zipfolder = zipname
    pswd = password
    pathfolder = tofolder

    with zipfile.ZipFile(zipfolder) as file:
        # password you pass must be in the bytes you converted 'str' into 'bytes'
        file.extractall(path = pathfolder, pwd = bytes(pswd, 'utf-8'))
            
def clean_up_file():
    try:
        #move the encrypted_uploadfolder to done_analyse
        for zipname in os.listdir(MAL_WORK_FOLDER):
            if ".zip" in zipname:
                print(zipname)
                shutil.copy(MAL_WORK_FOLDER + zipname, DONE_ANALYZED_FOLDER)
        for filename in os.listdir(RESULT_FOLDER):
            shutil.copy(RESULT_FOLDER+filename, DONE_ANALYZED_FOLDER+filename)
        #delete all files in malware_beware/
        os.chmod(MAL_UNZIP_FOLDER, mode=777)
        for zipname in os.listdir(MAL_UNZIP_FOLDER):
            os.remove(MAL_UNZIP_FOLDER+zipname)
        for zipname in os.listdir(MAL_WORK_FOLDER):
            if "unzip" not in zipname:
                os.remove(MAL_WORK_FOLDER+zipname)
    except Exception as e:
        print(e)