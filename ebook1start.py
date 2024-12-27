import requests
import argparse
import sys
import re  # regex
from bs4 import BeautifulSoup
import subprocess
import os

import ebook1F


book_id = 8154
#pstart = None
#pend = None

# for loveread.ec (ebook1F.py)
#example ## python3 start.py id=332 page=1-80

def start():

    if (len(sys.argv) > 1):
        argID = sys.argv[1]
    if ("id=" not in argID):
        argID = "id=" + input("Enter book_id: ")
    
    # Використовуємо регулярний вираз для отримання тільки цифр після 'id='
    match = re.search(r'id=(\d+)', argID)
    if match:
        argID = match.group(1)  # залишаємо тільки цифри
        book_id = argID

    # Обробка параметра p
    if len(sys.argv) > 2:
        p_arg = sys.argv[2]
        if ("page=" not in p_arg):
         p_arg = input("Enter page(№-№ of №): ")
        # Перевіряємо, чи є діапазон p
        match_p = re.match(r'page=(\d+)-(\d+)', p_arg)
        if match_p:
            pstart = int(match_p.group(1))
            pend = int(match_p.group(2)) + 1
        else:
            # Якщо p не є діапазоном, то це одиничне число
            match_p_single = re.match(r'page=(\d+)', p_arg)
            if match_p_single:
                pstart = int(match_p_single.group(1))
                pend = pstart + 1  # Якщо одиничне значення, то pend буде на 1 більше

    # Виводимо значення
    print(f"ID: {ebook1F.book_id}")
    ebook1F.book_id = book_id
    print(f"ID: {book_id}")
    print(f"ID: {ebook1F.book_id}")
    print(f"ID: {argID}")
    if pstart is not None and pend is not None:
        print(f"pstart: {pstart}")
        print(f"pend: {pend}")
        ebook1F.pstart = pstart
        ebook1F.pend = pend
    ebook1F.main()







# Функція для конвертації Calibre2
def convert_txt_to_mobi(txt_file, mobi_file):
    try:
        # Викликаємо Calibre для конвертації --authors=ebook1F.author --title=ebook1F.title
        command = ['ebook-convert', txt_file, mobi_file, f'--authors={ebook1F.author}', f'--title={ebook1F.title}']
        subprocess.run(command, check=True)
        print(f"Конвертація завершена: {mobi_file}")
    except subprocess.CalledProcessError as e:
        print(f"Помилка під час конвертації: {e}")




# Основна функція
def main():
    start()
    # Ініціалізуємо парсер аргументів
    #parser = argparse.ArgumentParser(description="Конвертування з TXT в MOBI")
    #parser.add_argument("txt_file", help="Шлях до TXT файлу")
    
    # Отримуємо аргумент командного рядка
    #args = parser.parse_args()
    
    # Генеруємо ім'я вихідного файлу (MOBI) на основі вхідного файлу
    #txt_filename = os.path.basename(args.txt_file)  # Отримуємо ім'я файлу без шляху
    txt_filename = ebook1F.filename
    print(f"{txt_filename}")
    title1 = os.path.splitext(txt_filename)[0]  # Видаляємо розширення файлу
    mobi_file = f"{title1}.mobi"  # Формуємо ім'я для MOBI файлу

    # Викликаємо функцію конвертації
    convert_txt_to_mobi(txt_filename, mobi_file)

if __name__ == "__main__":
    main()