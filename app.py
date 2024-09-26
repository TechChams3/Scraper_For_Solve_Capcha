from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
import tensorflow as tf
from keras import layers
import numpy as np
import os

app = Flask(__name__)

class CTCLayer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(CTCLayer, self).__init__(**kwargs)
        self.loss_fn = tf.keras.backend.ctc_batch_cost

    def call(self, y_true, y_pred):
        batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
        input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
        label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")
        input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
        label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")
        loss = self.loss_fn(y_true, y_pred, input_length, label_length)
        self.add_loss(loss)
        return y_pred

# Load the model
model = load_model('captcha_model.h5', custom_objects={'CTCLayer': CTCLayer})

# Create prediction model
prediction_model = tf.keras.models.Model(model.input[0], model.get_layer(name="dense2").output)

# Define character mappings
labels = ['2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'c', 'j', 's', 'u', 'w', 'x', 'y']
characters = sorted(set(char for label in labels for char in label))
max_length = 6
char_to_num = layers.StringLookup(vocabulary=list(characters), mask_token=None)
num_to_char = layers.StringLookup(vocabulary=char_to_num.get_vocabulary(), mask_token=None, invert=True)

def preprocess_image(img_path, img_width=200, img_height=50):
    img = tf.io.read_file(img_path)
    img = tf.io.decode_png(img, channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, [img_height, img_width])
    img = tf.transpose(img, perm=[1, 0, 2])
    return img

def decode_batch_predictions(pred, num_to_char, max_length):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    results = tf.keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][:, :max_length]
    char_list = num_to_char.get_vocabulary()

    output_text = []
    for result in results:
        result_text = ''.join([char_list[int(x)] for x in result if int(x) != -1])
        output_text.append(result_text)

    return output_text

def predict_text_from_image(img_path):
    img = preprocess_image(img_path)
    img = tf.expand_dims(img, axis=0)
    pred = prediction_model.predict(img)
    pred_texts = decode_batch_predictions(pred, num_to_char, max_length)
    return pred_texts[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    img_path = 'static/uploaded_image.png'
    file.save(img_path)

    predicted_text = predict_text_from_image(img_path)
    return jsonify({'predicted_text': predicted_text})

if __name__ == '__main__':
    app.run(debug=True)