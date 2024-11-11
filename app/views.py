from flask import Blueprint, render_template, current_app
from .models import News

main = Blueprint('main', __name__)

@main.route('/')
def index():
    pageType = 'index'
    title = 'اخبار روز'
    news = News.query.order_by(News.created_at.desc()).limit(current_app.config['POSTS_PER_PAGE'])
    return render_template('blog/index.html', news=news, pageType=pageType, title=title)

@main.route('/read/<int:id>')
def read(id):
    pageType ='read'
    title = 'جزئیات خبر'
    news = News.query.get_or_404(id)
    return render_template('blog/single.html', pageType=pageType, title=title, news=news)

@main.route('/news')
def news():
    pageType = 'news'
    title = 'لیست اخبار'
    return render_template('blog/news.html', pageType=pageType, title=title)

@main.route('/save')
def save():
    pageType = 'save'
    title = 'خبرهای ذخیره شده'
    return render_template('blog/save.html', pageType=pageType, title=title)

@main.route('/search')
def search():
    pageType = 'search'
    title = 'جستجو'
    return render_template('blog/news.html', pageType=pageType, title=title)