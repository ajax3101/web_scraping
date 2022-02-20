import random
from time import sleep
import encodings
import requests
from bs4 import BeautifulSoup
import json

"""
#########################
Предложенный  функционал!
#########################

def get_page_content(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    page_info = {
        "url": link,  # ссылка на новость
        "title": "",  # заголовок новости
        "img": "",  # ссылка на изображение
        "body": "",  # текст новости
        "author": "",  # автор новости (если указывается)
        "date": "",  # дата публикации новости в формате YYYY-MM-DD
        "time": "",  # время публикации новости в формате HH:MM
    }

    # ...

    return page_info


def get_links():
    r = requests.get(seed)
    # ...
    # ['https://www.news.com/pag1', 'https://www.news.com/pag2', ...]
    return []


def main():
    links = get_links()
    top_news = []
    for link in links:
        print(f"Обрабатывается {link}")
        info = get_page_content(link)
        top_news.append(info)

    with open("www-news-com.json", "wt") as f:
        json.dump(top_news, f)
    print("Работа завершена")

# Главная функция
if __name__ == "__main__":
    main()

"""

# url2 = "http://itnews.com.ua/news/"
headers = {
   "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
}

# req = requests.get(url2, headers=headers)
# src = req.text
# #print(src)

# with open("index.html", "w") as file:
#     file.write(src)
# with open("index.html") as file:
#     src = file.read()

# soup = BeautifulSoup (src, 'lxml', exclude_encodings=["utf-8"])
# all_news_hrefs = soup.find_all("h2")
# all_news_dict={}
# for item in all_news_hrefs:
#     #print(item)
#     item_text = item.text
#     #print(item_text)
#     item_href = 'http://itnews.com.ua' + item.find('a').get('href')
#     #print(item_href)
#     #print(f"{item_text}: {item_href}")
#     all_news_dict[item_text]=item_href

# with open('all_news_dict.json', 'w' ) as file:
#     json.dump(all_news_dict, file, indent=4, ensure_ascii=False)
with open('all_news_dict.json') as file:
    all_news = json.load(file)
#print(all_news)

iteration_count = int(len(all_news)) - 1
count = 0
print(f"Всего итераций: {iteration_count}")

for cat_news, cat_href in all_news.items():

    rep = [",", " ", "-", "'"]
    for item in rep:
        if item in cat_news:
            cat_news = cat_news.replace(item, "_")

    req = requests.get(url=cat_href, headers=headers)
    src = req.text

    with open(f"data/{count}_{cat_news}.html", "w") as file:
        file.write(src)
    

    with open(f"data/{count}_{cat_news}.html") as file:
        src = file.read()
    soup = BeautifulSoup (src, "lxml")
    
    page_info_dict = []

    page_info = soup.find(class_="article text")
    #print(page_info)
    #url = 
    title = page_info.find(class_="fg").text
    #print(title)
    img = page_info.find('img', src=True)
    #print(img['src'])
    body = page_info.find(itemprop="articleBody").text
    #print(body)
    #author = 
    data = page_info.find(class_="dt").text
    #print(data)
    #time = soup.find(class_="dt").text
    #print(time)
    page_info_dict.append (
        {
            # "Url": link,  # ссылка на новость
            "Title": title,  
            "Img": img['src'], 
            "Body": body,  
            "Date": data  
        }
    )
    with open(f"data/{count}_{cat_news}.json", "a", encoding="utf-8") as file:
        json.dump(page_info_dict, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"# Итерация {count}. {cat_news} записан...")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Работа завершена")
        break

    print(f"Осталось итераций: {iteration_count}")
    sleep(random.randrange(2, 4))