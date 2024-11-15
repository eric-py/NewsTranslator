from app import create_app
from app.scraper import run_scraper

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        run_scraper()