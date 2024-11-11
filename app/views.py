from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    pageType = 'index'
    return render_template('blog/index.html', pageType=pageType)

@main.route('/read')
def read():
    pageType ='read'
    return render_template('blog/single.html', pageType=pageType)

@main.route('/news')
def news():
    pageType = 'news'
    return render_template('blog/news.html', pageType=pageType)

@main.route('/save')
def save():
    pageType = 'save'
    return render_template('blog/save.html', pageType=pageType)

@main.route('/search')
def search():
    pageType = 'search'
    return render_template('blog/news.html', pageType=pageType)