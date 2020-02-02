from urllib.request import urlopen
from mysql.connector import connection
from bs4 import BeautifulSoup
import settings

try:
    soup = BeautifulSoup(urlopen("https://www.reserved.com/pl/pl/kids/all/").read(), "html.parser")

    items = soup.find_all("article")

    conn = connection.MySQLConnection(user=settings.user, password=settings.password, host=settings.host,
                                      database=settings.database, charset=settings.charset)

    cursor = conn.cursor()

    add_item = "insert into items(name_item, price_item, img_item, code_item) values (%s,%s,%s,%s)"

    for item in items:
        name = item.figure.figcaption.a.text
        price = str(item.figure.section.p.span.text).split()[0].replace(",", ".")
        img = item.figure.a.img['data-back-src']
        code = item['data-sku']
        data_item = (name, price, img, code)
        cursor.execute(add_item, data_item)
        print(data_item)
    conn.commit()
    cursor.close()
    conn.close()
except:
    print("Connection error")
