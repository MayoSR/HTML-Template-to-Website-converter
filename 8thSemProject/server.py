from flask import Flask, request,render_template
import os
app = Flask(__name__, static_url_path='')

app.config['UPLOAD_FOLDER'] = 'sketches'

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/sendfile', methods=['POST'])
def get_file():
    print(request.files)
    latestfile = request.files['uploaded-file']
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], "generatedpage.jpg")
    latestfile.save(full_filename)
    return 'file uploaded successfully'

@app.route('/generatedpage')
def get_page():
    return render_template(os.path.join("templates","generatedpage.html"))



if __name__ == "__main__":
    app.run(debug=True)