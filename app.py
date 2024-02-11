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
    # Text content to be downloaded
    content = """
    Precautions:
    Utilize pathogen-free seeds and disease-free transplants whenever possible to minimize the risk of bacterial spot.
    Avoid sprinkler irrigation and the accumulation of cull piles near greenhouse or field operations to prevent disease spread.
    Rotate crops with non-host plants to break the disease cycle and reduce pathogen buildup in the soil.

    Pesticides:
    Copper Hydroxide (Kocide 3000): Apply at a rate of 0.75–1.75 lb per acre. This multi-site contact fungicide acts as a protectant against bacterial spot. It has a restricted entry interval (REI) of 48 hours and no preharvest interval (PHI).

    Copper Hydroxide (Kocide 3000) + Mancozeb (Dithane M-45, Dithane F-45 Rainshield, Penncozeb 75DF): This combination enhances the efficacy of copper in controlling bacterial spot. Copper is applied at the same rate as above, while mancozeb is applied at a rate of 2 lb or 1.6 qt per acre. Both products have an REI of 24 hours and a PHI of 5 days.

    Disclaimer: It is essential to adhere to label instructions and consult with agricultural experts or local extension services before applying pesticides. Consider environmental impact and follow all safety precautions during pesticide application.

    Please note that the information provided is based on UC IPM Pest Management Guidelines for Tomato and should be used as a reference for disease management practices.
    """
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads, filename)

if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host='0.0.0.0', port=5000) #local host
    # app.run(host='0.0.0.0', port=8080) #for AWS
    # app.run(host='0.0.0.0', port=80) #for AZURE

