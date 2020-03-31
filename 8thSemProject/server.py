from flask import Flask, request, render_template
from modules.objectdetection import split_images
from modules.SVM import make_prediction
import os
from PIL import Image

app = Flask(__name__, static_url_path='')

app.config['UPLOAD_FOLDER'] = 'sketches'

def server_reset():
    fp = open(os.path.join("templates","content.html"),"w")
    fp.close()
    fp = open(os.path.join("static","styles","index.css"),"w")
    fp.close()
    for i in os.listdir(os.path.join(os.path.dirname(__file__), 'samples')):
        os.remove(os.path.join(os.path.join(os.path.dirname(__file__), 'samples'),i))
        

@app.route('/')
def root():
    return render_template('index.html')


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
