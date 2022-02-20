import requests
from bs4 import BeautifulSoup
import json
import random
from time import sleep
import requests


headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
}

'''
Первый блок (часть) программы
Сбор url всех новостей 
'''
# news_url_list = []

# for i in range(0, 1000):
#     url = f"https://www.zr.ru/news/?p={i}"
#     print(i)
#     sleep(random.randrange(2, 4))
#     q = requests.get(url, headers=headers)
#     result = q.content

#     soup = BeautifulSoup(result, 'lxml')
#     all_news = soup.find_all(class_="articles__item-ttl")
# #    print (all_news)

#     for news in all_news:
#         news_page_url = 'https://www.zr.ru' + news.find('a').get('href')
#         news_url_list.append(news_page_url)

# with open('www-zr-ru.txt', 'a') as file:
#     for line in news_url_list:
#         file.write(f'{line}\n')
'''
Второй блок (часть) программы
Сбор остальных данных 
'''
with open('www-zr-ru.txt') as file:
    lines = [line.strip() for line in file.readlines()]

    page_info_dict = []
    iteration_count = int(len(lines)) - 1
    count = 0
    print(f"Всего итераций: {iteration_count}")
    

    for line in lines:
        
        q = requests.get(line, headers=headers)
        result = q.content
    
        soup = BeautifulSoup(result, 'lxml')
        title = soup.find(class_="head").text
        try:
            img = soup.find(
                "div", class_="image-micro-schema").find("img").get("src")
        except Exception:
            img = "No images"
        try:
            video = 'https:' + \
                soup.find(
                    "div", class_="video-micro-schema").find("iframe").get("src")
        except Exception:
            video = "No video"
        body = soup.find("div", class_="article__intro").text + \
            soup.find("div", class_="content").text
        author = soup.find("div", class_="info__author").text
        date = soup.find(class_="d-day").text + \
            soup.find(class_="d-month").text+soup.find(class_="d-year").text

        page_info = {
            "url": line,  # ссылка на новость
            "title": title,  # заголовок новости
            "img": img,  # ссылка на изображение
            "video": video,  # ссылка на video
            "body": body,  # текст новости
            "author": author,  # автор новости (если указывается)
            "date": date,  # дата публикации новости
        }

        
        page_info_dict.append(page_info)

        with open('www-zr-ru.json', 'a', encoding="utf-8") as json_file:
            json.dump(page_info_dict, json_file, indent=4, ensure_ascii=False)
        
        count += 1
        print(f"# Итерация {count}: {line} записан...")
        iteration_count = iteration_count - 1

        if iteration_count == 0:
            print("Работа завершена")
            break

        print(f"Осталось итераций: {iteration_count}")
        sleep(random.randrange(2, 4))
