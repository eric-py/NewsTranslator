from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    pageType = 'index'
    title = 'اخبار روز'
    return render_template('blog/index.html', pageType=pageType, title=title)

@main.route('/read')
def read():
    pageType ='read'
    title = 'جزئیات خبر'
    return render_template('blog/single.html', pageType=pageType, title=title)

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