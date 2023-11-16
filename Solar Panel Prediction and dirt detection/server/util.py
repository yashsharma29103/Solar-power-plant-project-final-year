"""
@author: YASH_SHARMA
"""
import os
from flask import flash
from werkzeug.utils import redirect, secure_filename
from tensorflow.keras.models import load_model
import imageio as iio
import numpy as np
import pickle

def save_file(file):
    path = os.getcwd()
    UPLOAD_FOLDER = os.path.join(path, 'upload')
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        flash('File uploaded successfully')
    else:
        return redirect('service')
    


def begin_model():
    model = load_model('../model/model5.h5', compile=False)
    model.compile()
    return model
    
    

def dirt_detect(file):
    save_file(file)
    model = begin_model()
    path = os.getcwd()
    UPLOAD_FOLDER = os.path.join(path, 'upload')
    filename = secure_filename(file.filename)
    img = iio.imread(os.path.join(UPLOAD_FOLDER, filename))
    img = img/255
    img.resize(1,299, 299,3)
    prediction = model.predict(img)
    pred_classes = np.argmax(prediction, axis=1)
    class_names = ['Clean', 'Dusty']
    response = [class_names[pred_classes[0]], 100 * np.max(prediction)]
    print(response)
    
    return response

def begin_model2():
    model = load_model('../model/pred_model.h5', compile=False)
    model.compile()
    return model

def predict(X_test):
    model = begin_model2()
    with open('../model/sc.pkl','rb') as f:
        sc = pickle.load(f)
    X_test_scaled = sc.transform(X_test)
    res = model.predict(X_test_scaled)
    return res