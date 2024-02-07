import requests
import bs4
import fake_headers

# Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/articles/'


def gen_headers():
    headers_gen = fake_headers.Headers(os="win", browser="Microsoft Edge")
    return headers_gen.generate()


# создаем запрос
response = requests.get(URL, headers=gen_headers())
# получаем на выходе текстовую информацию
main_html = response.text
# создадим объект для хранения наших данных с полным списком статей
main_page = bs4.BeautifulSoup(main_html, "lxml")
# создадим переменную, в которой будут храниться все статьи
article_list_tag = main_page.find("div", class_="tm-articles-list")
article_body_tags = article_list_tag.find_all("article")

for article_tag in article_body_tags:
    h2_tag = article_tag.find("h2", class_="tm-title tm-title_h2") # заголовок
    a_tag = article_tag.find('a') # относительная ссылка
    time_tag = article_tag.find("time") # дата
    # извлекаем информацию
    pub_time = time_tag["datetime"]
    link_relative = a_tag["href"]
    link_absolute = f"https://habr.com{link_relative}"
    header = time_tag.text.strip()

    # вытащим текст
    response = requests.get(link_absolute, headers=gen_headers())
    article_html = response.text
    article_page = bs4.BeautifulSoup(article_html, "lxml")
    article_body_tag = article_tag.find(class_="article-formatted-body article-formatted-body "
                                               "article-formatted-body_version-2")
    article_text = article_body_tag.text.strip()

    for search_word in KEYWORDS:
        if (search_word in header) or (search_word in article_text):
            print(f'Дата: {pub_time} - Заголовок: {header} - Ссылка: {link_absolute}')



