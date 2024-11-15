from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/static/uploads'
    TEMPLATES_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/templates'
    STATIC_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/static'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(os.path.abspath(os.path.dirname(__file__)), 'news.db')
    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE'))
    BOT_USERNAME = os.environ.get('BOT_USERNAME')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    USE_AI_CATEGORIES = os.environ.get('USE_AI_CATEGORIES', 'False').lower() == 'true'