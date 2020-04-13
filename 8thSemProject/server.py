from flask import Flask, request, render_template, jsonify
from modules.objectdetection import split_images
from modules.SVM import make_prediction
import os
from PIL import Image
import json

app = Flask(__name__, static_url_path='')

app.config['UPLOAD_FOLDER'] = 'sketches'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def server_reset():
    fp = open(os.path.join("templates", "content.html"), "w")
    fp.close()
    fp = open(os.path.join("static", "styles", "index.css"), "w")
    fp.close()
    fp = open(os.path.join("metadata", "element_structure.json"), "w")
    fp.close()
    fp = open(os.path.join("metadata", "metadata.pkl"), "wb")
    fp.close()
    for i in os.listdir(os.path.join(os.path.dirname(__file__), 'samples')):
        os.remove(os.path.join(os.path.join(
            os.path.dirname(__file__), 'samples'), i))

def rewrite_css(data):
    fp = open(os.path.join("static", "styles", "index.css"), "r")
    fp_content = fp.read().replace("}", "} ").split()
    fp.close()
    reppos = -1
    for i in enumerate(fp_content):
        if data["ele"] in i[1]:
            reppos = i[0]
    ele = data["ele"]
    del data["ele"]
    fp_content[reppos] = ele+json.dumps(data).replace(",", ";").replace(
        " ", "").replace('"', '').replace("backgroundColor", "background-color")
    with open(os.path.join("metadata", "element_structure.json"), 'r') as f:
        json_css = json.load(f)
        for i in data:
            json_css[ele][i] = data[i]
    with open(os.path.join("metadata", "element_structure.json"), 'w') as f:
        json.dump(json_css, f)
    fp = open(os.path.join("static", "styles", "index.css"), "w")
    fp.write("".join(fp_content))
    fp.close()


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
    for name, value in globals().copy().items():
        print(name, value)
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
    return render_template("generatedpage.html")


if __name__ == "__main__":
    server_reset()
    app.run(debug=True)
