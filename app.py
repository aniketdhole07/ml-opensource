from flask import Flask, render_template, request
import PIL.ImageOps
from PIL import Image
from IPython.core.interactiveshell import InteractiveShell
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython import get_ipython
import pickle as cPickle
import os
from werkzeug.utils import secure_filename

#get_ipython().run_line_magic('matplotlib', 'inline')
InteractiveShell.ast_node_interactivity = "all"

app = Flask(__name__)


@app.route('/')
def man():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/img_classifier')
def img_classifier():
    return render_template("image_classifiers.html")


@app.route('/linear_reg')
def linear_reg():
    return render_template("linear_reg.html")


@app.route('/deepl')
def deepl():
    return render_template("decision_trees.html")


@app.route('/mnist_predict', methods=['POST', 'GET'])
def mnist():
    if request.method == 'POST':
        file = request.files['nm']
        basepath = os.path.dirname(__file__)
        #file.save(os.path.join(basepath, "uploads", file.filename))
        #user = os.path.join(basepath, "uploads", file.filename)
        file.save(os.path.join(basepath, file.filename))
        user = file.filename

        # load the model from disk
        model_name = 'Compressed-Models/finalized_model2.sav'
        loaded_model = cPickle.load(open(model_name, 'rb'))

        # preprocessing
        image = Image.open(user)
        p = plt.imshow(np.asarray(image), cmap=plt.cm.gray,)
        p = plt.title('Shape: ' + str(np.asarray(image).shape))

        # convert to grayscale image - 'L' format means each pixel is
        # represented by a single value from 0 to 255
        image_bw = image.convert('L')
        p = plt.imshow(np.asarray(image_bw), cmap=plt.cm.gray,)
        p = plt.title('Shape: ' + str(np.asarray(image_bw).shape))
        # resize image
        image_bw_resized = image_bw.resize((28, 28), Image.ANTIALIAS)
        p = plt.imshow(np.asarray(image_bw_resized), cmap=plt.cm.gray,)
        p = plt.title('Shape: ' + str(np.asarray(image_bw_resized).shape))

        # invert image, to match training data

        image_bw_resized_inverted = PIL.ImageOps.invert(image_bw_resized)
        p = plt.imshow(np.asarray(image_bw_resized_inverted),
                       cmap=plt.cm.gray,)
        p = plt.title(
            'Shape: ' + str(np.asarray(image_bw_resized_inverted).shape))

        # adjust contrast and scale
        pixel_filter = 20  # value from 0 to 100 - may need to adjust this manually
        min_pixel = np.percentile(image_bw_resized_inverted, pixel_filter)
        image_bw_resized_inverted_scaled = np.clip(
            image_bw_resized_inverted-min_pixel, 0, 255)
        max_pixel = np.max(image_bw_resized_inverted)
        image_bw_resized_inverted_scaled = np.asarray(
            image_bw_resized_inverted_scaled)/max_pixel
        p = plt.imshow(np.asarray(image_bw_resized_inverted_scaled),
                       cmap=plt.cm.gray,)
        p = plt.title(
            'Shape: ' + str(np.asarray(image_bw_resized_inverted_scaled).shape))

        # finally, reshape to (1, 784) - 1 sample, 784 features
        test_sample = np.array(
            image_bw_resized_inverted_scaled).reshape(1, 784)
        p = plt.imshow(np.reshape(test_sample, (28, 28)), cmap=plt.cm.gray,)
        p = plt.title('Shape: ' + str(test_sample.shape))
        p = plt.imshow(np.reshape(test_sample, (28, 28)), cmap=plt.cm.gray,)
        p = plt.title('Shape: ' + str(test_sample.shape))

        model = cPickle.load(open(model_name, 'rb'))
        test_pred = model.predict(test_sample)
        print("Predicted class is: ", test_pred)

        return render_template('image_classifiers.html', res=test_pred)


@app.route('/score_pred', methods=['POST', 'GET'])
def score_pred():
    if request.method == 'POST':
        model_name = 'Compressed-Models/model_lr.pkl'
        ml = cPickle.load(open(model_name, 'rb'))
        h0 = float(request.form.get('hours0'))
        s0 = ml.predict([[h0]])
        goal = float(request.form.get('goal'))
        diff = goal-s0
        #s0 = round(s0, 2)
        #diff = round(diff, 2)
        msg = ""
        if diff > 0:
            res_msg = "Sorry, not enough to reach your goal..Boost yourself! 💪"
        else:
            res_msg = "Great going!! Keep it up.."

        return render_template("linear_reg.html", res_msg=res_msg)


if __name__ == "__main__":
    app.run(debug=True)
