# TODO : Add labels/textbox
# TODO : Package HTML/CSS
# TODO : Decide removal of black/white filter
# TODO : Test with bad images
# TODO : Integrate Selenium

from flask import Flask, request, render_template, jsonify
from modules.objectdetection import split_images
from modules.SVM import make_prediction
import os
from PIL import Image
import json
from modules.resets import server_reset,reset_header,rewrite_css,download_file

app = Flask(__name__, static_url_path='')

app.config['UPLOAD_FOLDER'] = 'sketches'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/getcss', methods=['GET'])
def get_css():
    with open(os.path.join("metadata", "element_structure.json"), 'r') as f:
        return json.load(f)

@app.route('/modify', methods=['POST'])
def modify_css():
    json_str = request.get_json()
    rewrite_css(json_str)
    return render_template("generatedpage.html")

@app.route('/delete', methods=['GET'])
def delete_page():
    reset_header()
    server_reset()
    return "Page was cleared"

@app.route('/sendfile', methods=['POST'])
def get_file():
    server_reset()
    latestfile = request.files['uploaded-file']
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], "newimage.jpg")
    latestfile.save(full_filename)
    split_images()
    make_prediction()
    return 'File uploaded successfully'


@app.route('/generatedpage')
def get_page():
    download_file()
    return render_template("generatedpage.html")

@app.route("/download")
def download():
    download_file()
    return render_template("generatedpage.html")
    
    
if __name__ == "__main__":
    server_reset()
    app.run(debug=True)
