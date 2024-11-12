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

@main.route('/set_telegram_user_id', methods=['POST'])
def set_telegram_user_id():
    user_id = request.json.get('user_id')
    if user_id:
        session['telegram_user_id'] = user_id
        return jsonify({"success": True}), 200
    return jsonify({"success": False}), 400

@main.route('/toggle_save_news', methods=['POST'])
def toggle_save_news():
    user_id = session.get('telegram_user_id')
    news_id = request.json.get('news_id')

    user = User.query.filter_by(telegram_id=user_id).first()
    if not user:
        user = User(telegram_id=user_id)
        db.session.add(user)

    news = News.query.get(news_id)
    if not news:
        return jsonify({'success': False, 'message': 'خبر یافت نشد'}), 404

    if news in user.saved_news:
        user.saved_news.remove(news)
        is_saved = False
    else:
        user.saved_news.append(news)
        is_saved = True

    db.session.commit()
    return jsonify({'success': True, 'is_saved': is_saved})

@main.route('/check_save_status')
def check_save_status():
    user_id = session.get('telegram_user_id')
    news_id = request.args.get('news_id')

    user = User.query.filter_by(telegram_id=user_id).first()
    news = News.query.get(news_id)

    if not user or not news:
        return jsonify({'is_saved': False})

    is_saved = news in user.saved_news
    return jsonify({'is_saved': is_saved})