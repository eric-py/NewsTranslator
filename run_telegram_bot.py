from app import create_app
from app.telegram_handlers import main

app = create_app()

if __name__ == '__main__':
    main(app)