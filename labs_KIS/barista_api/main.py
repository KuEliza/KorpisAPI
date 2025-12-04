from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from barista_api.api.v1.api import *
import logging
from logging.handlers import RotatingFileHandler
import os

# Создаем директорию для логов если её нет
if not os.path.exists("logs"):
    os.makedirs("logs")


# Настройка логгирования
def setup_logging():
    # Создаем логгер
    logger = logging.getLogger("barista_api")
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(
        "logs/barista.log",
        maxBytes=1024 * 1024 * 5,
        backupCount=5
    )

    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


# Инициализируем логгер
logger = setup_logging()

app = FastAPI(
    title="Barista API",
    description="API для приложения Barista",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def home_page():
    return {"Текст": "Добро пожаловать в Barista API", "Управление": "http://127.0.0.1:8002/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
