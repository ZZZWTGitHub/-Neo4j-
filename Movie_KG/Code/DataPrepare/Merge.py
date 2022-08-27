# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 22:09:38 2022

@author: 30303
"""

import pandas as pd
import re

file_name = '..//..//Data//PreparedData//movie_data.csv'

csv_data = pd.read_csv(file_name, encoding='utf-8')
df = pd.DataFrame(csv_data, dtype=str)
film_dict = {}
director_list = []
scriptwriter_list = []
actor_list = []
type_list = []
country_list = []
for idx, data in df.iterrows():
    info_dict = {}
    film_name = data[1].split(' ')[0]
    film_year = data[2]
    info_dict['film_year'] = film_year

    l = data[3].split(' / ')
    save_l = []
    for s in l:
        if '?' in s:
            continue
        if s.strip() == '':
            continue
        inner = s.split('/')
        save_l.extend(inner)

    name = []
    for p in save_l:
        other_namelist = p.split(' (')
        if len(other_namelist) > 1:
            name.append(other_namelist[0])
        else:
            if '\u4e00' <= p[0] <= '\u9fa5':
                other_namelist = p.split(' ')
                name.append(other_namelist[0])
            else:
                name.append(p)
    info_dict['director'] = name
    director_list.extend(name)

    l = data[4].split(' / ')
    save_l = []
    for s in l:
        if '?' in s:
            continue
        if s.strip() == '':
            continue
        inner = s.split('/')
        save_l.extend(inner)
    name = []
    for p in save_l:
        other_namelist = p.split(' (')
        if len(other_namelist) > 1:
            name.append(other_namelist[0])
        else:
            if '\u4e00' <= p[0] <= '\u9fa5':
                other_namelist = p.split(' ')
                name.append(other_namelist[0])
            else:
                name.append(p)
    info_dict['scriptwriter'] = name
    scriptwriter_list.extend(name)

    l = data[5].split(' / ')
    save_l = []
    for s in l:
        if '?' in s:
            continue
        if s.strip() == '':
            continue
        inner = s.split('/')
        save_l.extend(inner)
    name = []
    for p in save_l:
        other_namelist = p.split(' (')
        if len(other_namelist) > 1:
            name.append(other_namelist[0])
        else:
            if len(p) > 0 and '\u4e00' <= p[0] <= '\u9fa5':
                other_namelist = p.split(' ')
                name.append(other_namelist[0])
            elif len(p) > 0:
                name.append(p)
    info_dict['actor'] = name
    actor_list.extend(name)

    l = data[6].split(' / ')
    save_l = []
    for s in l:
        if '?' in s:
            continue
        if s.strip() == '':
            continue
        inner = s.split('/')
        save_l.extend(inner)
        type_list.extend(inner)
    info_dict['film_type'] = save_l

    l = data[7].split(' / ')
    save_l = []
    for s in l:
        if '?' in s:
            continue
        if s.strip() == '':
            continue
        inner = s.split('/')
        save_l.append(inner[0])
        country_list.append(inner[0])
    info_dict['film_country'] = inner[0]

    l = data[8].split(' / ')
    save_l = []
    for s in l:
        if '?' in s:
            continue
        if s.strip() == '':
            continue
        inner = s.split('/')
        save_l.extend(inner)
    info_dict['film_language'] = save_l

    film_dict[film_name] = info_dict

type_list = list(set(type_list))
country_list = list(set(country_list))
country_clear = []
pattern = re.compile(r'[A-Za-z ]', re.S)
for country in country_list:
    res = re.findall(pattern, country)
    if len(res):
        continue
    if '中国' in country and country != '中国':
        continue
    country_clear.append(country)

type_list = [value for value in type_list if value != 'nan']
columns = ["type_name"]
dt = pd.DataFrame(type_list, columns=columns)
dt['Label'] = 'type'
dt.index.name = 'type_id'
dt.to_csv(r'..\..\Data\PreparedData\type.csv', encoding='utf-8')

columns = ["country_name"]
dt = pd.DataFrame(country_clear, columns=columns)
dt['Label'] = 'country'
dt.index.name = 'country_id'
dt.to_csv(r'..\..\Data\PreparedData\country.csv', encoding='utf-8')

director_list = [value for value in director_list if value != 'nan']
director_dict = {}
for director in director_list:
    director_dict[director] = director_dict.get(director, 0) + 1

dl = sorted(director_dict.items(), key=lambda x: x[1], reverse=True)
columns = ["director_name", "rank"]
dt = pd.DataFrame(dl, columns=columns)
dt['Label'] = 'director'
dt.index.name = 'director_id'
dt.to_csv(r'..\..\Data\PreparedData\director.csv', encoding='utf-8')

scriptwriter_list = [value for value in scriptwriter_list if value != 'nan']
scriptwriter_dict = {}
for scriptwriter in scriptwriter_list:
    scriptwriter_dict[scriptwriter] = scriptwriter_dict.get(scriptwriter, 0) + 1

ds = sorted(scriptwriter_dict.items(), key=lambda x: x[1], reverse=True)
columns = ["scriptwriter_name", "rank"]
dt = pd.DataFrame(ds, columns=columns)
dt['Label'] = 'scriptwriter'
dt.index.name = 'scriptwriter_id'
dt.to_csv(r'..\..\Data\PreparedData\scriptwriter.csv', encoding='utf-8')

actor_list = [value for value in actor_list if value != 'nan']
actor_dict = {}
for actor in actor_list:
    actor_dict[actor] = actor_dict.get(actor, 0) + 1

da = sorted(actor_dict.items(), key=lambda x: x[1], reverse=True)
columns = ["actor_name", "rank"]
dt = pd.DataFrame(da, columns=columns)
dt2 = dt[dt['rank'] > 1]
pactor = list(dt2['actor_name'])
dt['Label'] = 'actor'
dt.index.name = 'actor_id'
dt.to_csv(r'..\..\Data\PreparedData\actor.csv', encoding='utf-8')
dt2['Label'] = 'actor'
dt2.index.name = 'actor_id'
# dt2.to_csv('C:/Users/30303/Desktop/data/actor2.csv', encoding='utf-8')

movie_list = []
movie_director = []
movie_scriptwriter = []
movie_actor = []
movie_type = []
movie_country = []
for film in film_dict.keys():
    info_list = [film]
    info = film_dict[film]
    year = info['film_year']
    info_list.append(year)
    language = info['film_language']
    lan = ','.join(language)
    info_list.append(lan)
    movie_list.append(info_list)
    director = info['director']
    for dire in director:
        movie_director.append([film, dire])
    scriptwriter = info['scriptwriter']
    for scip in scriptwriter:
        movie_scriptwriter.append([film, scip])
    actor = info['actor']
    for act in actor:
        if act in pactor:
            movie_actor.append([film, act])
    film_type = info['film_type']
    for typ in film_type:
        movie_type.append([film, typ])
    country = info['film_country']
    if '中国' in country:
        country = '中国'
    movie_country.append([film, country])

columns = ["movie_name", "year", "language"]
df = pd.DataFrame(movie_list, columns=columns)
df['Label'] = 'movie'
df.index.name = 'movie_id'
df.to_csv(r'..\..\Data\PreparedData\movie.csv', encoding='utf-8')

columns = ["movie_name", "director"]
df = pd.DataFrame(movie_director, columns=columns).drop_duplicates()
df['Label'] = 'direct'
df.to_csv(r'..\..\Data\PreparedData\movie_director.csv', encoding='utf-8', index=False)

columns = ["movie_name", "scriptwriter"]
df = pd.DataFrame(movie_scriptwriter, columns=columns).drop_duplicates()
df['Label'] = 'writescript'
df.to_csv(r'..\..\Data\PreparedData\movie_scriptwriter.csv', encoding='utf-8', index=False)

columns = ["movie_name", "actor"]
df = pd.DataFrame(movie_actor, columns=columns).drop_duplicates()
df['Label'] = 'act'
df.to_csv(r'..\..\Data\PreparedData\movie_actor2.csv', encoding='utf-8', index=False)

columns = ["movie_name", "film_type"]
df = pd.DataFrame(movie_type, columns=columns).drop_duplicates()
df['Label'] = 'movietype'
df.to_csv(r'..\..\Data\PreparedData\movie_type.csv', encoding='utf-8', index=False)

columns = ["movie_name", "country"]
df = pd.DataFrame(movie_country, columns=columns).drop_duplicates()
df['Label'] = 'moviecountry'
df.to_csv(r'..\..\Data\PreparedData\movie_country.csv', encoding='utf-8', index=False)
