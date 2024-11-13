from flask import Blueprint, current_app, jsonify
from .models import News

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