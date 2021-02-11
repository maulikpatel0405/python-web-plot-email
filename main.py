import requests
import bs4
import matplotlib.pyplot as plt
import datetime
import csv
import re

search = input("Input proper stock code:")
url = "https://www.marketwatch.com/investing/stock/" + search + "?mod=over_search"
prev_sec = 0
sec = 1
datetime_object = datetime.datetime.now()
x = [60 * datetime_object.minute]
s_value = []


def web_scrapping():
    web_article = requests.get(url)
    web_article_lxml = bs4.BeautifulSoup(web_article.text, "lxml")
    header_web_article_lxml = web_article_lxml.find_all('h3')
    header_web_article_lxml_str = str(header_web_article_lxml[2]) + str(header_web_article_lxml[3])
    matches = re.findall(r'>.+?<', header_web_article_lxml_str)
    v = matches[1].replace('>', '')  # some times it works for #2, #3 indexes also.
    v = v.replace('<', '')
    stock_value = v.replace(',', '')
    stock_value_float = float(stock_value)
    print(stock_value_float, end=' ')
    s_value.append(stock_value_float)
    plt.plot(x, s_value)
    # plt.scatter(sec + 60*datetime_object.minute, stock_value_float)
    plt.pause(2)
    # plt.show()
    x.append(sec + 60 * datetime_object.minute)
    return stock_value


def file_writing(lull):
    with open("stock_price.csv", 'a+') as f:
        c_writer = csv.writer(f)
        c_writer = csv.writer(f, delimiter=' ')
        c_writer.writerow(lull)
    return c_writer


with open("stock_price.csv", 'w', newline='') as f:
    csv_writer = csv.writer(f)
    # file object created

if datetime_object.hour < 18:
    while True:
        datetime_object = datetime.datetime.now()
        sec = datetime_object.second
        scrapper = web_scrapping()
        f_writer = file_writing(scrapper)
