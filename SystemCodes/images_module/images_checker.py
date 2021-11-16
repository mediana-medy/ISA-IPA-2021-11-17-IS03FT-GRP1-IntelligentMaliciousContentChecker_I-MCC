import io
import os, sys
import logging
import zipfile
from google.cloud import vision_v1

client = vision_v1.ImageAnnotatorClient.from_service_account_json(
    "images_module\sigma-freedom-326000-91cabbbc8b4f.json")


def createzip(source_dir, output_filename):
    zip = zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED)
    # pre_len = len(os.path.dirname(source_dir))
    for path, dirnames, filenames in os.walk(source_dir):
        fpath = path.replace(source_dir, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()


def one_safe_search_detection(image):
    """Detects unsafe features in the file."""

    with io.open(image, 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    return safe


def folder_detection(folderpath):
    for filename in os.listdir(folderpath):
        if not (filename.endswith('.jpg') | filename.endswith('.JPG')):
            continue
        # Read the input file
        print("processing: " + filename)
        filepath = folderpath + '/' + filename
        safe = one_safe_search_detection(filepath)
        likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                           'LIKELY', 'VERY_LIKELY')
        l1 = 'LIKELY'
        l2 = 'VERY_LIKELY'
        if likelihood_name[safe.adult] == l1 or likelihood_name[safe.adult] == l2 or likelihood_name[
            safe.violence] == l1 or likelihood_name[safe.violence] == l2 or likelihood_name[safe.racy] == l1 or \
                likelihood_name[safe.racy] == l2:
            os.remove(filepath)
            print("delete: " + filename)
            logging.info(filepath)


def unzip(zipname, tofolder):
    zipfolder = zipname
    pathfolder = tofolder

    with zipfile.ZipFile(zipfolder) as file:
        # password you pass must be in the bytes you converted 'str' into 'bytes'
        file.extractall(path=pathfolder)
