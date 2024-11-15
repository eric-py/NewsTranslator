from flask import current_app
from .models import db, NewsLink, News, Category
from urllib.parse import urljoin
from lxml import html, etree
from datetime import datetime
from bs4 import BeautifulSoup
from functools import lru_cache
from deep_translator import GoogleTranslator
import google.generativeai as genai
import trafilatura
import re, time

def scrape_hacker_news(n=10):
    base_url = 'https://thehackernews.com/'
    news_links = []
    downloaded = trafilatura.fetch_url(base_url)
    if downloaded is None:
        return []
    tree = html.fromstring(downloaded)
    for element in tree.xpath('//a[@class="story-link"]'):
        href = element.get('href')
        if href and href.startswith('https://thehackernews.com/20'):
            full_url = urljoin(base_url, href)
            if full_url not in news_links:
                news_links.append(full_url)
                if len(news_links) >= n:
                    break
    return news_links[:n]

def get_category(title, article_tags):
    use_ai_categories = current_app.config.get('USE_AI_CATEGORIES', False)
    
    if use_ai_categories:
        genai.configure(api_key=current_app.config.get('GOOGLE_API_KEY', None))
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        Read the following text carefully and identify its category. Respond only with the category name(s) in Persian, without any additional text or explanation. If there are multiple categories, separate them with commas(،).

        Title: {title}
        Categories: {','.join(article_tags)}

        Output (Persian category name(s) only, separated by commas(،) if multiple):
        """
        try:
            response = model.generate_content(prompt)
            ai_categories = {cat.strip() for cat in response.text.split('،') if cat.strip()} if response and response.text else set()
            return ai_categories
        except Exception:
            print("خطا در دریافت دسته‌بندی از هوش مصنوعی. استفاده از دسته‌بندی‌های اصلی.")
    
    translated_tags = {translate_text(tag, 'title') for tag in article_tags}
    return translated_tags


def extract_news_content(url):
    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        return None

    tree = html.fromstring(downloaded)
    
    title = tree.xpath('//h1[@class="story-title"]/a/text() | //h1[@class="story-title"]/text()')[0].strip() if tree.xpath('//h1[@class="story-title"]/a/text() | //h1[@class="story-title"]/text()') else "عنوان نامشخص"
    image_url = tree.xpath('//div[@class="story-image"]/img/@data-src | //meta[@property="og:image"]/@content')[0] if tree.xpath('//div[@class="story-image"]/img/@data-src | //meta[@property="og:image"]/@content') else None
    
    date = None
    date_element = tree.xpath('//div[@class="postmeta"]//span[@class="author"]/text()')
    if date_element:
        try:
            date = datetime.strptime(date_element[0].strip(), '%b %d, %Y')
        except ValueError:
            pass

    content_elements = tree.xpath('//div[contains(@class, "separator")]/following-sibling::*[self::p or self::h1 or self::h2 or self::h3 or self::h4][following::div[@class="stophere"]]')
    if content_elements:
        content = ''.join([re.sub(r'<(?!/?(?:p|h[1-4])(?=>|\s))[^>]+>', '', etree.tostring(elem, encoding='unicode')) for elem in content_elements])
    else:
        content = "محتوا در دسترس نیست"

    tags = tree.xpath('//span[@class="p-tags"]/text()')
    article_tags = [tag.strip() for tag in (tags[0].split(' / ') or tags[0].split('/'))] if tags else []

    categories = get_category(title, article_tags)    
    translated_title = translate_text(title, 'title')
    translated_content = translate_text(content, 'content')

    return {
        'title': translated_title,
        'date': date,
        'content': translated_content,
        'image_url': image_url,
        'categories': categories
    }

@lru_cache(maxsize=1000)
def cached_translate(text):
    translator = GoogleTranslator(source='en', target='fa')
    return translator.translate(text)

def translate_text(text, type):
    if type == 'title':
        try:
            return cached_translate(text)
        except Exception:
            return text
    
    elif type == 'content':
        soup = BeautifulSoup(text, 'html.parser')
        elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4'])
        
        batch_size = 10
        translated_content = []
        
        for i in range(0, len(elements), batch_size):
            batch = elements[i:i+batch_size]
            batch_text = [elem.text for elem in batch]
            
            try:
                translated_batch = [cached_translate(t) for t in batch_text]
                translated_content.extend([f"<{batch[j].name}>{translated}</{batch[j].name}>" for j, translated in enumerate(translated_batch)])
                time.sleep(0.5)
            except Exception:
                translated_content.extend([str(elem) for elem in batch])
        
        return ''.join(translated_content)
    
    else:
        raise ValueError("نوع متن نامعتبر است. باید 'title' یا 'content' باشد.")

def process_news(url):
    existing_link = NewsLink.query.filter_by(url=url).first()
    if existing_link:
        return

    news_data = extract_news_content(url)
    if news_data is None:
        return

    try:
        new_news = News(
            title=news_data['title'],
            content=news_data['content'],
            news_date=news_data['date'],
            image_url=news_data['image_url']
        )

        db.session.add(new_news)
        db.session.flush()

        categories = news_data['categories']
        for category_name in categories:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
            new_news.categories.append(category)

        new_link = NewsLink(url=url, news=new_news)
        db.session.add(new_link)

        db.session.commit()
        print(f"خبر جدید با عنوان '{new_news.title}' ذخیره شد.")

    except Exception as e:
        db.session.rollback()
        print(f"خطا در ذخیره‌سازی خبر: {e}")
        
def run_scraper(n=10):
    print(f"\n{'='*50}")
    print(f"  شروع اسکرپ کردن {n} خبر")
    print(f"{'='*50}\n")

    links = scrape_hacker_news(n)
    links.reverse()
    total_links = len(links)
    
    for index, link in enumerate(links, start=1):
        print(f"لینک {index}/{total_links}:")
        print(f"{link}")
        process_news(link)
        print(f"{'*'*30}")
        time.sleep(1)
    
    print(f"\n{'='*50}")
    print(f"  پایان اسکرپ کردن {total_links} خبر")
    print(f"{'='*50}\n")