from sentence_transformers import SentenceTransformer
import torch
import numpy as np
import tensorflow as tf
import warnings
warnings.filterwarnings('ignore')
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# hello test git
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'yo'
db = SQLAlchemy(app)
# one user has many posts, one post only has 1 user,
# 1 to many model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True) #?

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

posts = [
    {
        'author': 'Nikhil Gaur',
        'title':  'I love Dallas Mavericks',
        'body': 'I really love the Dallas Mavericks, I have been watching them since I was a child',
        'date': '12/26/2020'
    },
    {
        'author': 'Himanshu Gaur',
        'title':  'Dallas Mavericks suck now',
        'body': 'Dallas Mavericks have had a really rough go since their win in 2011, failing to get past the first round ever since, have not even made it into playoffs since then, Luka Doncic addition has been sort of helpful',
        'date': '12/26/2020'
    }
]

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        users = User.query.filter_by(username=username).all()
        if len(users) > 0:
            print('Successfully connected existing user')
            return redirect(url_for("home",username=username,password=password,email=email))
        else:
            return redirect(url_for("register"))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        users = User.query.filter_by(username=username).all()
        if len(users) == 0:
            user = User(username=username,password=password,email=email)
            db.session.add(user)
            db.session.commit()
            print("Successfully added new user to system")
            flash("Successfully added new user to system")
            return redirect(url_for("home",username=username,password=password,email=email))
        else:
            print("Error User Already exists")
            flash(f"User {username} already exists in the system, this action is for new users","error")
            return render_template('register.html')

@app.route('/home/<username>',methods=['GET','POST'])
def home(username):
    #print('Retrieved form data')

    #posts = Post.query.filter_by(user_id=user.id).all()
    #print('Committing User')
    #flash('Your ')
    return render_template('home.html',username=username,posts=posts,num_posts=len(posts))

def get_wing(text):
    embedding_model = SentenceTransformer(model_name_or_path='bert-base-nli-mean-tokens',
                                          device=torch.device('cpu'))
    embeddings = embedding_model.encode(text)
    embeddings = np.transpose(np.array(embeddings).reshape(-1, 1))
    new_model = tf.keras.models.load_model('my_model.h5')
    x = new_model.predict_classes(embeddings)
    return 'right' if x[0][0] == 1 else 'left'

@app.route('/submit', methods=['GET','POST'])
def submit():
    text = request.form['text']
    wing = get_wing(text)
    title = request.form['title']
    # add to database
    #user = User()
    return render_template('post.html',title=title, text=text, wing=wing.upper())
    #return '<h1> Post: {} </h1><br></br><h1>This post belongs to a {} winger </h1>'.format(text,wing)

@app.route('/new_post',methods=['GET','POST'])
def new_post():
    return render_template('new_post.html')

if __name__ == '__main__':
    app.run(debug=False) #change to false when just checking to see how it works, true for actual debugging
    db.create_all()