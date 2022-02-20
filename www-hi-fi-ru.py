import json
import time
from turtle import title
from urllib import response
from wsgiref import headers
import requests
from bs4 import BeautifulSoup
import datetime

start_time = time.time()


def get_data():
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    url = 'https://www.hi-fi.ru/news/page-1/'

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    page_count = int(
        soup.find("div", class_="pagination").find_all("a")[-1].text)
    # print(page_count)
    all_news_data_dict = []

    # for page in range (1, page_count+1):
    for page in range(1, 2):
        url = f'https://www.hi-fi.ru/news/page-{page}/'

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        news_items = soup.find_all("div", class_="list-item")
        for ni in news_items:
            news_data = ni.find("div", class_="content")
            # print(news_data)
            try:
                title = news_data.find("h3", class_="title").text.strip()
            except:
                title = "Нет названия"
            try:
                url_title = "https://www.hi-fi.ru" + \
                    news_data.find("a").get('href').strip()
                r = requests.get(url=url_title, headers=headers)
                sup = BeautifulSoup(r.text, "lxml")
                try:
                    img = sup.find(
                        "div", class_="news-item").find("img").get("src")
                except Exception:
                    img = "No images"
                body = sup.find(
                    "div", class_="news-item__content").text.strip()
            except:
                url_title = "Нет URLa"
            try:
                data = news_data.find("div", class_="category").text.strip()
            except:
                data = "Нет Даты"
            # print(title)
            # print(url_title)
            # print(data)
            # print("#"*20)

            all_news_data = {
                "Url_Title": url_title,
                "Title": title,
                "Image_URL": img,
                "Body": body,
                "Data": data
            }
            all_news_data_dict.append(all_news_data)

            print(f"Обработана {page}/{page_count}")
            time.sleep(3)
    with open('wwww-hi-fi-ru.json', 'a', encoding="utf-8") as json_file:
        json.dump(all_news_data_dict, json_file, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"Затраченное время на работу скрипта: {finish_time}")


if __name__ == '__main__':
    main()
