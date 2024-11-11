from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .utils import time_passed

db = SQLAlchemy()

# Models
news_categories = db.Table('news_categories',
    db.Column('news_id', db.Integer, db.ForeignKey('news.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    news = db.relationship('News', secondary=news_categories, back_populates='categories')

class NewsLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False, unique=True)
    news = db.relationship('News', back_populates='link', uselist=False)

    def __repr__(self):
        return self.url

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    news_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(500))
    categories = db.relationship('Category', secondary=news_categories, back_populates='news')
    link = db.relationship('NewsLink', back_populates='news', uselist=False)

    def get_time_passed(self):
        return time_passed(self.created_at)