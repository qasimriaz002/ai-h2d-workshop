from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from werkzeug.utils import secure_filename

import tensorflow as tf

#Assume that the number of cores per socket in the machine is denoted as NUM_PARALLEL_EXEC_UNITS
#  when NUM_PARALLEL_EXEC_UNITS=0 the system chooses appropriate settings

app = Flask(__name__)

# Load the trained model
model = load_model('pneumonia_model.h5', compile=False)

# Render the home page
@app.route('/')
def home():
    return render_template('index.html')

# Handle the prediction
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the uploaded image file
        file = request.files['file']
        # Save the uploaded file
        file_path = 'static/' + secure_filename(file.filename)
        file.save(file_path)
         
        #patient data
        patient = {"name": request.form['name'], "age": request.form['age']}

        # Preprocess the image
        img = image.load_img(file_path, target_size=(64, 64))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img /= 255.0

        # Make predictions
        prediction = model.predict(img)
        result = "Pneumonia" if prediction > 0.5 else "Normal"
        color = "red" if prediction > 0.5 else "green"
        data = {"result":result, "img_path":file_path, "color":color, "patient":patient}
        return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
