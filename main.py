import json
import re
from pprint import pprint
import requests
import bs4
import fake_headers

URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'


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
vac_list_tag = main_page.find("div", id="a11y-main-content")
vac_body_tags = vac_list_tag.find_all("div", class_="serp-item")
vacancies = []


for vac_tag in vac_body_tags:
    span_tag = vac_tag.find("span", class_="serp-item__title")
    # название вакансии
    name_vac = span_tag.text.strip()
    # относительная ссылка на вакансию
    link_vac = vac_tag.find("a")["href"]
    link_true_vac = f"https://spb.hh.ru{link_vac}"
    # зарплата
    span_tag_salary = vac_tag.find("span", class_="bloko-header-section-2")
    span_tag_salary = (re.sub('\u202f', '', span_tag_salary.text.strip())
                       if span_tag_salary else "зарплата не указана")
    # организация
    organization_vac = vac_tag.find("a", class_="bloko-link bloko-link_kind-tertiary")
    organization_vac = (re.sub('\xa0', ' ', organization_vac.text.strip())
                        if organization_vac else "не указана")
    # город
    country_org = vac_tag.find("div", attrs={"data-qa": "vacancy-serp__vacancy-address"})
    country_org = (re.findall(r'^\w+-*\w*\b', country_org.text.strip())[0] if country_org else "город не указан")

    vacancies.append(
        {
            "name": name_vac,  # название вакансии
            "link": link_true_vac,  # ссылка на вакансию
            "salary": span_tag_salary,  # зарплата
            "organization": organization_vac,  # организация
            "address": country_org,  # город
        }
    )

pprint(vacancies, width=100, sort_dicts=False)

with open("vacancies.json", "w", encoding="utf-8") as file:
    json.dump(vacancies, file, indent=4, ensure_ascii=False)

