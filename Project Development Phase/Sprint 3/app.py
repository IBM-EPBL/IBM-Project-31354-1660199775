from flask import Flask, render_template, request
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import requests
import json
 
app = Flask(__name__)
model=load_model('nutrition.h5')
print("Loaded model from disk")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/uploader", methods = ["POST","GET"])
def uploader():
    if request.method == "POST":
        f = request.files["file"]
        f.save(f.filename)
        
        img=image.load_img(f.filename,target_size=(64,64))
        x=image.img_to_array(img)
        x=np.expand_dims(x,axis=0)

        pred=np.argmax(model.predict(x), axis=1)
        print("prediction",pred)
        index=['APPLE','BANANA','ORANGE','PINEAPPLE','WATERMELON']
        
        result=str(index[pred[0]])

        item = result

        return render_template("value.html",item=item)
    itemmsg = "Upload a valid image"
    return render_template("upload.html",itemmsg=itemmsg)

if __name__ == "__main__":
    app.run(use_reloader=True,debug=True)