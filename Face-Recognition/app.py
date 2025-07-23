from flask import Flask, render_template, request, redirect, url_for
from get_faces_from_camera_tkinter import Face_Register
import base64

import subprocess

app = Flask(__name__)

@app.route('/')
def index():

    with open('templates/p11.jpg', 'rb') as image_file:
        # Encode the image as Base64
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return render_template('index.html', base64_image=base64_image)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    subprocess.run(['python', 'get_faces_from_camera_tkinter.py'])

    return redirect(url_for('index'))

@app.route('/extract_features', methods=['POST'])
def extract_features():
    message = "Extration completed"
    subprocess.run(['python', 'features_extraction_to_csv.py'])
    
    return render_template('index.html', message=message)

@app.route('/detect_faces', methods=['POST'])
def detect_faces():
    subprocess.run(['python', 'detect.py'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
