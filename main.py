import requests
import bs4
import matplotlib.pyplot as plt
import datetime
import csv
import re
# import sqlite3
import smtplib  # To send an email. to create an email.
# import imaplib  # To parse through your email for all the content - to check a sent email.
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formatdate
from email.encoders import encode_base64

search = input("Input proper stock code:")
url = "https://www.marketwatch.com/investing/stock/" + search + "?mod=over_search"
datetime_object = datetime.datetime.now()
s_value = []
x = [60 * datetime_object.minute]

with open('stock_price.csv', encoding='utf-8') as csv_object:
    csv.writer(csv_object, delimiter=' ')


def web_scrapping(boo_rl):
    stock_value = ''
    stock_value_float = 0.0
    temp_object = datetime.datetime.now()
    web_article = requests.get(boo_rl)
    web_article_lxml = bs4.BeautifulSoup(web_article.text, "lxml")
    header_web_article_lxml = web_article_lxml.find_all('h3')  # h2 header also has all the values.
    # print(header_web_article_lxml)
    header_web_article_lxml_str = str(header_web_article_lxml[2]) + str(header_web_article_lxml[3])
    # print(header_web_article_lxml_str)
    matches = re.findall(r'>.+?<', header_web_article_lxml_str)
    # print(matches)
    for count, i in enumerate(matches):
        v = matches[count].replace('>', '')  # some times it works for #2, #3 indexes also.
        v = v.replace('<', '')
        stock_value = v.replace(',', '')
        try:
            stock_value_float = float(stock_value)
            break
        except ValueError:
            continue
    # print('None of the values had the stock price: ')
    # print(stock_value_float, end=' ')
    s_value.append(stock_value_float)
    # print(s_value, x)
    plt.plot(x, s_value)
    # plt.scatter(sec + 60*datetime_object.minute, stock_value_float)
    plt.pause(1)
    # plt.show()
    x.append(sec + 60 * temp_object.minute)
    return stock_value


def file_writing(lull):
    file_list = []
    with open("stock_price.txt", 'a+') as f_w:
        c_writer = f_w.write(lull + ' ')
        t_bytes = f_w.tell()
    file_list.append(t_bytes)
    file_list.append(c_writer)
    return file_list


def file_reading(lull):
    with open("stock_price.txt", 'rb') as f_w:
        c_reader = f_w.read(lull)
        c_bytes = f_w.tell()
    return c_bytes, c_reader


def emailing(msg_attachment):

    msg_confirmation = 0
    smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
    e_c = smtp_object.ehlo()
    smtp_object.starttls()
    if e_c[0] == 250:
        # print('In the email area.')
        email = getpass.getpass(prompt='Please provide (Maulik) your email address: ')
        email1 = getpass.getpass(prompt='Please provide email address to whom you would like to sen an email to: ')
        password = getpass.getpass(prompt='Please provide (Maulik) your password: ')
        l_s = smtp_object.login(email, password)
        if l_s[0] == 235:
            print('Login successful in your gmail account and verified.')
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = email1
            msg['Cc'] = ''
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = 'Hello Friends!! A python scripted email.'
            part = MIMEBase('application', 'vnd.ms-excel')
            part.set_payload(msg_attachment)
            encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename='stock_price.txt')
            msg.attach(part)
            msg_confirmation = smtp_object.sendmail(email, email1.split(',') + msg['Cc'].split(','), msg.as_string())
            smtp_object.quit()
    return msg_confirmation


with open("stock_price.txt", 'w', newline='') as f:
    f.write('Hello!! This is the stock value file. ')

f_attachment = 0

if 8 < datetime_object.hour < 19:
    while True:
        datetime_object = datetime.datetime.now()
        sec = datetime_object.second
        scrapper = web_scrapping(url)
        f_writer = file_writing(scrapper)
        # print(" The stock values are being printed at this point in the real time every second. ")
        f_bytes, f_reader = file_reading(f_writer[0])
        # print(f_reader, f_bytes)
        if f_bytes >= 1:
            success = emailing(f_reader)
            f_reader = 0
            print(f' This is a success object returned by the SEND EMAIL METHOD. {success}')
