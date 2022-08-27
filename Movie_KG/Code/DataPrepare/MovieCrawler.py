# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 09:58:06 2022

@author: 30303
"""

import requests
from bs4 import BeautifulSoup
import csv

global f, f_csv


def download_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)"}
    return requests.get(url, headers=headers).content


def parse_timesmovie_html(html):
    soup = BeautifulSoup(html, 'html.parser')  # parse tool: BeautifulSoup
    page_soup = soup.find(class_='grid-16-8 clearfix')
    # find body
    for movie_li in page_soup.find_all(class_='info'):
        link = movie_li.find('a')
        url = link['href']
        parse_timesmovie_content(url)


def parse_timesmovie_content(html):
    this_row = [None for _ in range(9)]
    html_data = download_page(html)
    soup = BeautifulSoup(html_data, 'html.parser')  # parse tool: BeautifulSoup
    movie_soup = soup.find(class_='rating_self clearfix')
    movie_name_all = soup.find(property='v:itemreviewed').text
    this_row[0] = movie_name_all
    print(this_row[0])
    movie_rate = movie_soup.find(class_='ll rating_num').text
    print(movie_rate)
    this_row[1] = movie_rate

    f_csv.writerow(this_row)


def main():
    global f, f_csv
    print("----------------------start------------------------")
    page_url = 'https://movie.douban.com/top250?start='
    f = open(r"..\..\Data\NewKGData\movie.csv", "a+", encoding='utf-8', newline='')
    f_csv = csv.writer(f)

    # traverse all pages
    for i in range(189, 250, 25):
        html_data = download_page(page_url + str(i))
        parse_timesmovie_html(html_data)


if __name__ == '__main__':
    main()
