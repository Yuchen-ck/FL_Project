import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import pymongo
myclient = pymongo.MongoClient("mongodb://root:example@140.124.182.1:27017/")
mydb = myclient["FL"]
mycol = mydb["FL"]

UPLOAD_FOLDER = './FL'
app = Flask(__name__,static_folder='./static/',static_url_path='')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

@app.route("/uploadDB", methods=['POST'])
def up():
    try:
        data =request.get_json()
        mycol.insert_one(data)
        return "insert successs"
    except:
        return "insert error"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 6000)