from sentence_transformers import SentenceTransformer
import torch
import numpy as np
import tensorflow as tf
import warnings
warnings.filterwarnings('ignore')

from flask import Flask, request, render_template
post = 0
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    embedding_model = SentenceTransformer(model_name_or_path='bert-base-nli-mean-tokens',
                                          device=torch.device('cpu'))
    embeddings = embedding_model.encode(text)
    embeddings = np.transpose(np.array(embeddings).reshape(-1, 1))
    new_model = tf.keras.models.load_model('my_model.h5')
    x = new_model.predict_classes(embeddings)
    wing = x[0][0]
    wing = ''
    if x[0][0] == 1:
        wing = 'right'
    else:
        wing = 'left'

    return '<h1> Post: {} </h1><br></br><h1>This post belongs to a {} winger </h1>'.format(text,wing)

if __name__ == '__main__':
    app.run(debug=True)