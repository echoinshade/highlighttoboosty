import json
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Загружаем настройки из .env
load_dotenv()
BOOSTY_USERNAME = os.getenv("BOOSTY_USERNAME", "echoinshade")  # Никнейм с Boosty
VIDEO_INFO_FILE = "last_video.json"

# Загружаем данные о видео
def load_video_info():
    if not os.path.exists(VIDEO_INFO_FILE):
        print("❌ Файл с данными о видео не найден! Сначала скачайте видео.")
        exit()

    with open(VIDEO_INFO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Загрузка видео на Boosty
def upload_to_boosty(video_path, video_date):
    edge_options = Options()
    edge_options.debugger_address = "localhost:9223"
    driver = webdriver.Edge(options=edge_options)
    wait = WebDriverWait(driver, 15)

    boosty_url = f"https://boosty.to/{BOOSTY_USERNAME}/new-post"
    print(f"🌐 Открываем {boosty_url}...")
    driver.get(boosty_url)

    # Ожидание поля тегов
    tags_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'теги')]")))
    tags_field.send_keys("стрим")
    tags_field.send_keys(Keys.RETURN)

    date_tag = datetime.strptime(video_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y")
    tags_field.send_keys(date_tag)
    tags_field.send_keys(Keys.RETURN)

    # Ожидание поля заголовка
    title_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите заголовок поста']")))
    title_field.send_keys(os.path.basename(video_path))

    # Ожидание кнопки "Видео"
    video_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Видео')]]")))
    video_button.click()
    time.sleep(2)

    # Ожидание кнопки "Загрузить файлом"
    upload_file_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Загрузить файлом')]")))
    upload_file_button.click()

    # Загрузка файла
    file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
    file_input.send_keys(os.path.abspath(video_path))
    time.sleep(10)

    # Нажатие "Опубликовать"
    publish_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Опубликовать')]")))
    publish_button.click()

    print("✅ Видео загружено на Boosty!")
    driver.quit()

if __name__ == "__main__":
    video_info = load_video_info()
    upload_to_boosty(video_info["video_path"], video_info["video_date"])
