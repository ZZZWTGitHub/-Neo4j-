# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv

global f, f_csv


def download_page(url):
    headers = {
        "Cookie": 'll="108288"; bid=9ioZ1zZA8yk; dbcl2="256257563:JPE6SYmxb5Q"; ck=2Bis; push_noty_num=0; push_doumail_num=0',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54"
    }
    return requests.get(url, headers=headers).content


def parse_timesmovie_html(html):
    soup = BeautifulSoup(html, 'html.parser')  # parse tool: BeautifulSoup
    page_soup = soup.find(class_='grid-view')
    # find body
    for movie_li in page_soup.find_all(class_='title'):
        link = movie_li.find('a')
        url = link['href']
        #print(url)
        parse_timesmovie_content(url)


def parse_timesmovie_content(html):
    global f, f_csv
    this_row = [None for _ in range(9)]
    html_data = download_page(html)
    soup = BeautifulSoup(html_data, 'html.parser')  # parse tool: BeautifulSoup
    movie_soup = soup.find(class_='rating_self clearfix')
    movie_name = soup.find(property='v:itemreviewed').text
    this_row[0] = movie_name
    print(movie_name)
    movie_rate = movie_soup.find(class_='ll rating_num').text
    this_row[1] = movie_rate
    print(movie_rate)

    f_csv.writerow(this_row)


def main():
    print("----------------------start------------------------")

    page_url = 'https://movie.douban.com/people/69807491/collect?start='
    global f, f_csv
    f = open(r"..\..\Data\NewKGData\movie.csv", "a+", encoding='utf-8', newline='')
    f_csv = csv.writer(f)
    # traverse all pages
    for i in range(5730, 6800, 15):
        print(i)
        html_data = download_page(page_url + str(i) + '&sort=time&rating=all&filter=all&mode=grid')
        parse_timesmovie_html(html_data)
    f.close()


if __name__ == '__main__':
    main()
