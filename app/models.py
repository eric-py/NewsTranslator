from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from collections import Counter
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

saved_news = db.Table('saved_news',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('news_id', db.Integer, db.ForeignKey('news.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100))
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    saved_news = db.relationship('News', secondary=saved_news, back_populates='saved_by')

    def __repr__(self):
        return self.telegram_id

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    news_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    image_url = db.Column(db.String(500))
    categories = db.relationship('Category', secondary=news_categories, back_populates='news')
    link = db.relationship('NewsLink', back_populates='news', uselist=False)
    saved_by = db.relationship('User', secondary=saved_news, back_populates='saved_news')

    def get_time_passed(self):
        return time_passed(self.created_at)

    def category(self):
        return '، '.join([category.name for category in self.categories])
    
    def get_related_news(self, limit=3):
        related_ids = db.session.query(news_categories.c.news_id).filter(
            news_categories.c.category_id.in_([c.id for c in self.categories]),
            news_categories.c.news_id != self.id
        ).distinct().all()
        
        related_ids = [r[0] for r in related_ids]
        
        if not related_ids:
            return None
        
        category_counts = Counter()
        for news_id in related_ids:
            categories = db.session.query(news_categories.c.category_id).filter(
                news_categories.c.news_id == news_id,
                news_categories.c.category_id.in_([c.id for c in self.categories])
            ).all()
            category_counts[news_id] = len(categories)
        
        sorted_related_ids = sorted(category_counts, key=lambda x: (-category_counts[x], News.query.get(x).news_date), reverse=True)
        
        related_news = News.query.filter(News.id.in_(sorted_related_ids[:limit])).all()
        
        related_news.sort(key=lambda x: (-category_counts[x.id], x.news_date), reverse=True)
        
        return related_news