#ebook1F.py
import requests
import argparse
from bs4 import BeautifulSoup
book_id = 8154
pstart = 1
pend = 2 # №+1
filename = None
title = None
author = None

# Функція для обробки опису книги та отримання назви та автора
def get_book_details(book_id):
    url = f'http://loveread.ec/view_global.php?id={book_id}'
    
    # Виконуємо GET запит до сторінки
    response = requests.get(url)

    # Перевірка, чи вдалося отримати сторінку
    if response.status_code == 200:
        # Парсимо HTML контент
        soup = BeautifulSoup(response.text, 'html.parser')

        # Виводимо весь HTML для перевірки структури
        # print(soup.prettify())  # Uncomment for debugging

        # Шукаємо тег <span> з текстом "Название:" для отримання назви книги
        title_tag = soup.find('span', string=lambda text: text and "Название:" in text)
        if title_tag:
            title = title_tag.find_next('strong').get_text(strip=True) if title_tag else "Без назви"
        else:
            title = "Без назви"
        
        # Шукаємо тег <span> з текстом "Автор:" для отримання автора книги
        author_tag = soup.find('span', string=lambda text: text and "Автор:" in text)
        if author_tag:
            author = author_tag.find_next('a').find('strong').get_text(strip=True) if author_tag else "Автор не вказаний"
        else:
            author = "Автор не вказаний"

        return title, author
    else:
        print(f"Не вдалося завантажити сторінку опису книги. Статус: {response.status_code}")
        return None, None

# Функція для обробки сторінки та запису тексту в файл
def get_text_from_page(page_number, file):
    url = f'http://loveread.ec/read_book.php?id={book_id}&p={page_number}'
    
    # Виконуємо GET запит до сторінки
    response = requests.get(url)

    # Перевірка, чи вдалося отримати сторінку
    if response.status_code == 200:
        # Парсимо HTML контент
        soup = BeautifulSoup(response.text, 'html.parser')

        # Пошук всіх елементів <p> з класом 'MsoNormal'
        text_elements = soup.find_all('p', class_='MsoNormal')

        # Виведення тексту з кожного абзацу, додаємо два нових рядки для абзаців
        for idx, element in enumerate(text_elements):
            text = element.get_text(strip=True)
            if text:  # Перевірка на порожній текст
                if idx > 0:  # Пропускаємо перший абзац
                    file.write(text + "\n\n")  # Записуємо текст у файл з двома новими рядками
    else:
        print(f"Не вдалося завантажити сторінку {page_number}. Статус: {response.status_code}")

def main():
    global filename
    # Витягнення даних книги
    global title, author
    title, author = get_book_details(book_id)

    # Перевірка витягнутих даних
    print(f"Назва книги: {title}")
    print(f"Автор: {author}")



    # Заміна пробілів на підкреслення
    filename = f"book_{author.replace(' ', '_')}_{title.replace(' ', '_')}.txt"


    # Записуємо текст усіх сторінок в один файл
    with open(filename, "w", encoding="utf-8") as file:
        for page_number in range(pstart, pend):  # Для кожної сторінки від 1 до 81
            print(f"Завантаження сторінки {page_number}...")
            get_text_from_page(page_number, file)

    print(f"Текст успішно збережений у файл {filename}.")

if __name__ == "__main__":
    main()
