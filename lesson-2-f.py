import requests
import bs4
from urllib.parse import urljoin
import pymongo


def date_prepare(date):
    """ Обработка и получение старых и новых дат акций"""
    date = date.replace("с ", "", 1).replace("\n", "").split("до")
    try:        
        date_start = date[0]
        date_end = date[1]
        return date
    except IndexError:
        return date[0]



def new_price(new_price):
    """ Получение новых цен"""
    new_price = new_price.replace("\n", "")
    new_price = new_price[:2] + "." + new_price[2:]
    return new_price


# подключение к бд
db_client = pymongo.MongoClient()
db = db_client['gb_data_mining_dz']
collection = db['magnit']

# get запрос
url = "https://magnit.ru/promo/"
response = requests.get(url)

# получение списка всех продуктов
soup = bs4.BeautifulSoup(response.text, "lxml")
catalog_main = soup.find("div", attrs={"class": "сatalogue__main"})
product_tags = catalog_main.find_all("a", recursive=False)

# пустой лист для дальнейшего сохранения в него продуктов
product_list = []

# собираем всю информацию в переменную и добавляем в лист
for product in product_tags:
    product_dict = {}
    try:
        product_dict["product_name"] = product.find("div", attrs={"class": "card-sale__title"}).text
        product_dict["url"] = urljoin(url, product.attrs.get("href", ""))
        product_dict["promo_name"] = product.find("div", attrs={"class": "card-sale__header"}).text
        product_dict["image_url"] = urljoin(url,  product.find("img").attrs.get("data-src"))
        product_dict["old_price"] =  product.find("span", attrs={"class": "label__price-integer"}).text + "." + product_tags[0].find("span", attrs={"class": "label__price-decimal"}).text
        product_dict["new_price"] = new_price(product.find("div", attrs={"class": "label__price_new"}).text)

        date = date_prepare( product.find("div", attrs={"class": "card-sale__date"}).text)
        if len(date) == 2: #Если все нормально и у акции есть дата старта и окончания
            product_dict["date_start"] = date[0]
            product_dict["date_end"] = date[1]
        else: # если у даты нет даты окончания ( например дата только в один день)
            product_dict["date_start"] = date[0]
            product_dict["date_end"] = None

        #добавление в лист
        product_list.append(product_dict) 

    except AttributeError as error:
        pass # на случай, если при итерации попадемся на баннер

#Сохранение в бд
for element in product_list:
    collection.insert_one(element)