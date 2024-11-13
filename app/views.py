from flask import Blueprint, render_template, current_app, request, jsonify, session, redirect, url_for
from .models import News, db, User
from sqlalchemy import desc

main = Blueprint('main', __name__)

@main.route('/')
def index():
    news = News.query.order_by(News.created_at.desc()).limit(current_app.config['POSTS_PER_PAGE'])
    return render_template('blog/index.html', news=news, pageType='index', title='اخبار روز')

@main.route('/read/<int:id>')
def read(id):
    news = News.query.get_or_404(id)
    return render_template('blog/single.html', pageType='read', title='جزئیات خبر', news=news)

@main.route('/news')
def news():
    page = request.args.get('page', 1, type=int)
    pagination = News.query.order_by(News.created_at.desc()).paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'])
    return render_template('blog/news.html', pageType='news', title='لیست اخبار', pagination=pagination)

@main.route('/search')
def search():
    return render_template('blog/news.html', pageType='search', title='جستجو')

@main.route('/save')
def save():
    if 'telegram_user_id' not in session:
        return redirect(url_for('main.index'))
    
    user = User.query.filter_by(telegram_id=session['telegram_user_id']).first()
    if not user:
        return 'کاربر یافت نشد. لطفا با تلگرام وارد شوید.'
    
    page = request.args.get('page', 1, type=int)
    pagination = News.query.join(User.saved_news).filter(User.id == user.id).order_by(desc(News.created_at)).paginate(
        page=page, 
        per_page=current_app.config['POSTS_PER_PAGE']
    )
    return render_template('blog/news.html', pageType='save', title='خبرهای ذخیره شده', pagination=pagination)