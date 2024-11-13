from flask import Blueprint, current_app, jsonify, session, request
from .models import News, User, db

api = Blueprint('api', __name__)

@api.route('/bot_username', methods=['GET'])
def bot_username():
    bot_username = current_app.config['BOT_USERNAME']

    if bot_username:
        return jsonify({'bot_username': bot_username})
    else:
        return jsonify({'error': 'آیدی ربات را ست کنید.'}), 500

@api.route('/news/<int:news_id>', methods=['GET'])
def get_news(news_id):
    news = News.query.get_or_404(news_id)
    return jsonify({
        'id': news.id,
        'title': news.title,
        'image_url': news.image_url,
        'content': news.content,
    })

@api.route('/set_telegram_user_id', methods=['POST'])
def set_telegram_user_id():
    user_id = request.json.get('user_id')
    if user_id:
        session['telegram_user_id'] = user_id
        return jsonify({"success": True}), 200
    return jsonify({"success": False}), 400

@api.route('/toggle_save_news', methods=['POST'])
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

@api.route('/check_save_status')
def check_save_status():
    user_id = session.get('telegram_user_id')
    news_id = request.args.get('news_id')

    user = User.query.filter_by(telegram_id=user_id).first()
    news = News.query.get(news_id)

    if not user or not news:
        return jsonify({'is_saved': False})

    is_saved = news in user.saved_news
    return jsonify({'is_saved': is_saved})