# 🌐 مترجم اخبار | News Translator

**یک وب‌اپ تلگرامی هوشمند برای دریافت، ترجمه، و ارائه اخبار از منابع انگلیسی به فارسی**  
**A smart Telegram web app for retrieving, translating, and delivering news from English sources to Persian**

---

## 🎯 درباره پروژه | About the Project

**مترجم اخبار** یک ربات تلگرامی و وب‌اپ کاربردی است که با استفاده از **Flask** و **python-telegram-bot** توسعه یافته است.  
**News Translator** is a Telegram bot and web app built with **Flask** and **python-telegram-bot**. 

### قابلیت‌ها:  
- جمع‌آوری اخبار از منابع معتبر انگلیسی زبان ( ما در اینجا از **هکر نیوز** استفاده کردیم).  
- ترجمه اخبار به زبان فارسی.  
- دسته‌بندی اخبار با استفاده از **Gemini AI**.  
- ارائه تجربه کاربری روان و دوستانه در وب‌اپ.  

---

## ✨ ویژگی‌ها | Features

- **اسکرپ اخبار | News Scraping:** جمع‌آوری اخبار روز از منابع انگلیسی.  
  Scraping daily news from English sources.  

- **ترجمه خودکار | Auto Translation:** ارائه ترجمه روان و دقیق به فارسی.  
  Translating news accurately to Persian.  

- **دسته‌بندی اخبار با استفاده از جمنای | News Categorization with Gemini AI:**  
  اخبار به طور خودکار با استفاده از فناوری **Gemini AI** دسته‌بندی می‌شوند.  
  News is automatically categorized using **Gemini AI** technology.

- **وب‌اپ واکنش‌گرا | Responsive Web App:** با حالت **دارک مود** و **لایت مود** سازگار است.  
  Compatible with **Dark Mode** and **Light Mode** settings of Telegram.  

- **اشتراک‌گذاری | Sharing:** امکان به اشتراک‌گذاری اخبار با دیگران.  
  Easy sharing of news with others.  

- **ذخیره‌سازی | Saving:** ذخیره اخبار برای مطالعه در زمان دیگر.  
  Save news for later reading.  

---

## 🛠 پیش‌نیازها | Prerequisites

برای اجرای این پروژه به موارد زیر نیاز دارید:  
You need the following to run the project:  

- **Python 3.6+**  
- **pip**  
- **Node.js** and **npm**

---

## 🚀 نصب و راه‌اندازی | Installation & Setup

### 1️⃣ کلون کردن مخزن | Clone the Repository
```bash
git https://github.com/eric-py/NewsTranslator.git
cd NewsTranslator
```

### 2️⃣ نصب وابستگی‌های پایتون | Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ نصب وابستگی‌های Node.js | Install Node.js Dependencies
```bash
npm install
```

### 4️⃣ ساخت فایل‌های CSS با Tailwind | Build CSS with Tailwind
```bash
npm run build
```

### 5️⃣ تنظیم متغیرهای محیطی | Configure Environment Variables
فایل `.env_file` را به `.env` تغییر دهید و مقادیر زیر را در آن تنظیم کنید:  
Rename `.env_file` to `.env` and set the following values:

```env
SECRET_KEY = "کلید امنیتی برای Flask | Flask secret key"
TELEGRAM_TOKEN = "توکن ربات تلگرامی | Telegram bot token"
WEBAPP_URL = "آدرس وب‌اپ | Web app URL (e.g., https://your-app.herokuapp.com)"
POSTS_PER_PAGE = "تعداد پست‌ها در هر صفحه | Number of posts per page (e.g., 10)"
BOT_USERNAME = "نام کاربری ربات تلگرامی | Telegram bot username"
GOOGLE_API_KEY = "کلید API گوگل برای ترجمه | Google API key for translations"
USE_AI_CATEGORIES = "True برای فعال‌سازی دسته‌بندی با جمنای | Set to True to enable Gemini AI categorization"
```

---

## ▶️ اجرای پروژه | Running the Project

### 1️⃣ اجرای وب‌اپ Flask | Run the Flask Web App
```bash
python run.py
```

### 2️⃣ اجرای ربات تلگرامی | Run the Telegram Bot
```bash
python run_telegram_bot.py
```

### 3️⃣ اجرای اسکریپت اسکرپ و ترجمه اخبار | Run the Scraper Script
```bash
python run_scraper.py
```

---

## 🕒 تنظیم تسک‌های خودکار | Scheduling Automated Tasks

برای اجرای خودکار اسکریپت اسکرپ اخبار، می‌توانید از ابزارهای زمان‌بندی استفاده کنید:  
To automate news scraping, use scheduling tools such as:  

- **Linux/MacOS:** استفاده از `cron` | Using `cron`  
- **Windows:** استفاده از **Task Scheduler** | Using **Task Scheduler**

---

## 💻 تکنولوژی‌های استفاده‌شده | Technologies Used

- **Python**: زبان برنامه‌نویسی اصلی | Main programming language  
- **Flask**: فریم‌ورک توسعه وب | Web framework  
- **python-telegram-bot**: کتابخانه مدیریت ربات تلگرامی | Telegram bot library  
- **TailwindCSS**: برای طراحی واکنش‌گرا | For responsive design  
- **Trafilatura / BeautifulSoup**: برای اسکرپ اخبار | For scraping news  
- **Gemini AI**: برای دسته‌بندی اخبار | For news categorization  

---

## 📜 لایسنس | License

این پروژه تحت [GPL-3.0](LICENSE) منتشر شده است.  
This project is licensed under the [GPL-3.0](LICENSE).