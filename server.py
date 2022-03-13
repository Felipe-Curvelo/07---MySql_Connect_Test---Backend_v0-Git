from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin

import os

load_dotenv()

app = Flask(__name__)
CORS(app)




######################################## mysql://username:password@server/db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+ os.getenv("DB_USERNAME") + ':' + os.getenv("DB_PASSWORD") + '@' + os.getenv("DB_SERVER") + '/' + os.getenv("DB_NAME")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())

    def __init__(self, title, body):
        self.title = title
        self.body = body

class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body' )

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route("/get", methods = ['GET'])
@cross_origin()
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)

@app.route("/get/<id>/", methods = ['GET'])
@cross_origin()
def post_details(id):
    article = Articles.query.get(id)
    return article_schema.jsonify(article)

@app.route("/add", methods = ['POST'])
@cross_origin()
def add_article():
    title = request.json['title']
    body = request.json['body']

    articles = Articles(title, body)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)

@app.route("/update/<id>/", methods = ['PUT'])
@cross_origin()
def update_article(id):
    article = Articles.query.get(id)

    title = request.json['title']
    body = request.json['body']

    article.title = title
    article.body = body

    db.session.commit()
    return article_schema.jsonify(article)

@app.route("/delete/<id>/", methods = ['DELETE'])
@cross_origin()
def delete_article(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()

    return article_schema.jsonify(article)


##############
if __name__ == "__main__":
    app.run()