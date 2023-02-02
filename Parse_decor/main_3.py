# Задание 3.

from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import os


def logger(old_function):
    def new_function(*args, **kwargs):
        data_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        name_func = old_function.__name__
        res = old_function(*args, **kwargs)
        with open("main.log", "a", encoding='UTF-8') as file:
            file.write(f'Дата и время вызова функции {name_func}: {data_time}\n')
            file.write(f'Аргументы функции  {name_func}: {args}, {kwargs}\n')
            file.write(f'Результат работы {name_func}:\n {res}\n')
            # for item in res:
            #     file.write(item)
        return res

    return new_function


@logger
def main():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)
    path1 = "./div[@class='vacancy-serp-item-body']/div/div[3]/span"
    path2 = "./div[@class='vacancy-serp-item-body']/div/div[4]/div/div[2]"
    url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    KEYWORDS = ['Джанго', 'джанго', 'Flask', 'flask', 'Django', 'django', 'фласк', 'Фласк']
    json = dict.fromkeys(['Ссылка', 'Вилка зп', 'Название компании', 'Город'])
    driver = webdriver.Chrome()
    driver.get(url)
    res = driver.find_element(By.ID, 'HH-React-Root').find_elements(By.CLASS_NAME, 'vacancy-serp-item__layout')
    lst = []
    lst1 = []

    for item in res:
        json['Ссылка'] = ''
        for var in KEYWORDS:
            if not json['Ссылка']:
                if var in item.text:
                    json['Ссылка'] = item.find_element(By.CLASS_NAME, 'serp-item__title').get_attribute('href')

                    try:
                        json['Вилка зп'] = item.find_element(By.XPATH, path1).text.replace(u'\u202f', '')
                    except Exception:
                        json['Вилка зп'] = 'Не указано'

                    json['Название компании'] = item.find_element(By.CLASS_NAME, 'bloko-text').text
                    try:
                        json['Город'] = item.find_element(By.XPATH, path2).text
                    except Exception:
                        json['Город'] = 'Город не указан'

        if json['Ссылка']:
            lst.append(json)

    return lst


if __name__ == '__main__':
    main()
