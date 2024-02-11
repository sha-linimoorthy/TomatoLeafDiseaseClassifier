from flask import Flask, request, jsonify, render_template, send_from_directory, current_app
import os
from flask_cors import CORS, cross_origin
from cnnClassifier.utils.common import decodeImage
from cnnClassifier.pipeline.predict import PredictionPipeline

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = r'.\upload_folder'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline(self.filename)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/train", methods=['GET','POST'])
@cross_origin()
def trainRoute():
    os.system("python main.py")
    return "Training done successfully!"



@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    image = request.json['image']
    decodeImage(image, clApp.filename)
    result = clApp.classifier.predict()
    return jsonify(result)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads, filename)

@app.route('/download/precautions', methods=['GET'])
def download_precautions():
    # Path to the precautions file
    precautions_file = r'D:\classifier\TomatoLeafDiseaseClassifier\upload_folder\precautions.txt'
    return send_from_directory(app.root_path, precautions_file, as_attachment=True)

if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host='0.0.0.0', port=5000) #local host
    # app.run(host='0.0.0.0', port=8080) #for AWS
    # app.run(host='0.0.0.0', port=80) #for AZURE

