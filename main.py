from sentence_transformers import SentenceTransformer
import torch
import numpy as np
import tensorflow as tf
import warnings
warnings.filterwarnings('ignore')
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from newspaper import Article
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'yo'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True) #?
    articles = db.relationship('News',backref='reader',lazy=True)
    num_right_articles = db.Column(db.Integer, default=0)
    num_left_articles = db.Column(db.Integer, default=0)
    num_right_posts = db.Column(db.Integer, default=0)
    num_left_posts = db.Column(db.Integer, default=0)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    wing = db.Column(db.String(20))

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keywords = db.Column(db.Text)
    description = db.Column(db.Text)
    summary = db.Column(db.Text)
    title = db.Column(db.Text)
    reader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)




@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('login.html') #login.html originally
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        users = User.query.filter_by(username=username).all()
        if len(users) > 0:
            return redirect(url_for("home",username=username))
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
            flash("Successfully added new user to system")
            return redirect(url_for("home",username=username))
        else:
            flash(f"User {username} already exists in the system, this action is for new users","error")
            return render_template('register.html')

@app.route('/home/<username>',methods=['GET','POST'])
def home(username):
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        if 'text' in request.form and 'title' in request.form:
            text = request.form['text']
            title = request.form['title']
            flash("You have successfully made a post on PoliticAI!",'success')
            post = Post(user_id=user.id, title=title, body=text)
            post.wing = get_wing(text)
            db.session.add(post)
            db.session.commit()
        if 'news_link' in request.form:
            link = request.form['news_link']
            article = Article(link)
            article.download()
            article.parse()
            article.nlp()
            keywords = ''
            for word in article.keywords:
                keywords += word
                keywords += ', '
            news_article = News(keywords=keywords,description=article.meta_description,summary=article.summary,title=article.title,reader_id=user.id)
            db.session.add(news_article)
            db.session.commit()

    posts = Post.query.all()
    return render_template('home.html',username=username,posts=posts,news_articles=user.articles)

def get_wing(text):
    embedding_model = SentenceTransformer(model_name_or_path='bert-base-nli-mean-tokens',
                                          device=torch.device('cpu'))
    embeddings = embedding_model.encode(text)
    embeddings = np.transpose(np.array(embeddings).reshape(-1, 1))
    new_model = tf.keras.models.load_model('my_model.h5')
    x = new_model.predict_classes(embeddings)
    return 'right' if x[0][0] == 1 else 'left'

@app.route('/user/<username>',methods=['GET','POST'])
def user(username):
    news_sources = []
    if request.method == 'POST':
        print('Getting News Sources')
        news_sources = request.form.getlist('news-checkbox')
    print(news_sources)
    return render_template("user.html",username=username,news_sources=news_sources)

if __name__ == '__main__':
    app.run(debug=False) #change to false when just checking to see how it works, true for actual debugging
    db.create_all()