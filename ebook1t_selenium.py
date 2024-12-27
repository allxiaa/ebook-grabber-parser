from selenium import webdriver
from bs4 import BeautifulSoup
import time
# for loveread.ec
# Налаштування драйвера Selenium (потрібно встановити веб-драйвер, наприклад, ChromeDriver)
driver = webdriver.Chrome()

# Перебір сторінок
with open("book_text_selenium.txt", "w", encoding="utf-8") as file:
    for page_number in range(1, 82):  # Для кожної сторінки від 1 до 81
        print(f"Завантаження сторінки {page_number}...")
        url = f'http://loveread.ec/read_book.php?id=8154&p={page_number}'
        driver.get(url)

        # Чекаємо кілька секунд, поки JavaScript завантажить сторінку
        time.sleep(3)

        # Отримуємо HTML код сторінки
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Пошук тексту на сторінці
        text_elements = soup.find_all('p', class_='MsoNormal')
        for element in text_elements:
            text = element.get_text(strip=True)
            if text:
                file.write(text + "\n\n")

driver.quit()
print("Текст успішно збережений у файл 'book_text_selenium.txt'.")
