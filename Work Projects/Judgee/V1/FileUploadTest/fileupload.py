# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

import os
from flask import Flask, flash, request, redirect, url_for
from google.cloud import storage
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    
    if request.method == 'POST':
        file = request.files['file']
        data = file.read()
        
        f = open("./downloadedFiles/" + file.filename, "wb")
        f.write(data)
        f.close()
        
        client = storage.Client.from_service_account_json('benkey.json')
        bucket = client.get_bucket('profile_photos777')
        blob = bucket.blob("/" + file.filename)
        blob.upload_from_filename(filename="./downloadedFiles/" + file.filename)
        
        return "Got file " + file.filename + " which contained:<br>" + str(data)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


def downloadFileFromCloud(name):
	assert type(name) == str
	client = storage.Client.from_service_account_json('benkey.json')
	bucket = client.get_bucket('profile_photos777')
	blob = bucket.get_blob("/" + name)
	f = open("./downloadedFiles/" + name, "wb")
	blob.download_to_file(f)

app.debug = True
app.run()
