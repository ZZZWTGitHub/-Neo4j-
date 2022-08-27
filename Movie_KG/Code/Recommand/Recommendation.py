# -*- coding: utf-8 -*-
"""
Created on Thu May  5 11:29:32 2022

@author: 30303
"""
from py2neo import Graph
import pandas as pd
import math
import csv


def recommend(graph, movie):
    core_type = graph.evaluate(
        "MATCH p=(m1:Movie)-[r1:movie_type]-(a:Type) where m1.name='{name}' RETURN count(a)*25".format(name=movie))
    core_actor = graph.evaluate(
        "MATCH p=(m1:Movie)-[r1:movie_actor]-(a:Actor) where m1.name='{name}' RETURN sum(a.rank*a.rank)".format(
            name=movie))
    core_director = graph.evaluate(
        "MATCH p=(m1:Movie)-[r1:movie_director]-(a:Director) where m1.name='{name}' RETURN sum(a.rank*a.rank)".format(
            name=movie))
    core_scriptwriter = graph.evaluate(
        "MATCH p=(m1:Movie)-[r1:movie_scriptwriter]-(a:Scriptwriter) where m1.name='{name}' RETURN sum(a.rank*a.rank)".format(
            name=movie))
    core_total = core_type + core_actor + core_director + core_scriptwriter
    # print(core_total)

    df_a = pd.DataFrame(graph.run(
        "MATCH p=(m1:Movie)-[r1:movie_actor]-(a:Actor)-[r2:movie_actor]-(m2:Movie) where m1.name='{name}' RETURN "
        "a.name,a.rank,m2.name".format(name=movie))
        , columns=["a_name", "a_rank", "m_name"])

    dict_cos = {}
    dict_mov = {}
    list_mov = []

    for index, row in df_a.iterrows():
        name = row["m_name"]
        list_mov.append(name)
        if name in dict_cos.keys():
            dict_cos[name] += row["a_rank"] * row["a_rank"]
        else:
            dict_cos[name] = row["a_rank"] * row["a_rank"]

    df_d = pd.DataFrame(graph.run(
        "MATCH p=(m1:Movie)-[r1:movie_director]-(a:Director)-[r2:movie_director]-(m2:Movie) where m1.name='{name}' "
        "RETURN a.name,a.rank,m2.name".format(name=movie))
        , columns=["d_name", "d_rank", "m_name"])

    for index, row in df_d.iterrows():
        name = row["m_name"]
        list_mov.append(name)
        if name in dict_cos.keys():
            dict_cos[name] += row["d_rank"] * row["d_rank"]
        else:
            dict_cos[name] = row["d_rank"] * row["d_rank"]

    df_s = pd.DataFrame(graph.run(
        "MATCH p=(m1:Movie)-[r1:movie_scriptwriter]-(a:Scriptwriter)-[r2:movie_scriptwriter]-(m2:Movie) where "
        "m1.name='{name}' RETURN a.name,a.rank,m2.name".format(name=movie))
        , columns=["s_name", "s_rank", "m_name"])

    for index, row in df_s.iterrows():
        name = row["m_name"]
        list_mov.append(name)
        if name in dict_cos.keys():
            dict_cos[name] += row["s_rank"] * row["s_rank"]
        else:
            dict_cos[name] = row["s_rank"] * row["s_rank"]

    df_t = pd.DataFrame(graph.run(
        "MATCH p=(m1:Movie)-[r1:movie_type]-(a:Type)-[r2:movie_type]-(m2:Movie) where m1.name='{name}' RETURN a.name,"
        "m2.name".format(name=movie))
        , columns=["type", "m_name"])

    for index, row in df_t.iterrows():
        name = row["m_name"]
        list_mov.append(name)
        if name in dict_cos.keys():
            dict_cos[name] += 25
        else:
            dict_cos[name] = 25

    list_mov = list(set(list_mov))
    for movie in list_mov:
        cypher_a = "MATCH p=(m1:Movie)-[r1:movie_actor]-(a:Actor) where m1.name='{name}' RETURN sum(a.rank*a.rank)".format(
            name=movie)
        cypher_d = "MATCH p=(m1:Movie)-[r1:movie_director]-(a:Director) where m1.name='{name}' RETURN sum(" \
                   "a.rank*a.rank)".format(
            name=movie)
        cypher_s = "MATCH p=(m1:Movie)-[r1:movie_scriptwriter]-(a:Scriptwriter) where m1.name='{name}' RETURN sum(" \
                   "a.rank*a.rank)".format(
            name=movie)
        cypher_t = "MATCH p=(m1:Movie)-[r1:movie_type]-(a:Type) where m1.name='{name}' RETURN count(a)*25".format(
            name=movie)
        count = graph.evaluate(cypher_a)
        count += graph.evaluate(cypher_d)
        count += graph.evaluate(cypher_s)
        count += graph.evaluate(cypher_t)
        dict_mov[movie] = count
    dict_res = {}
    for movie in dict_cos.keys():
        dict_res[movie] = dict_cos[movie] / (math.sqrt(core_total) * math.sqrt(dict_mov[movie]))

    dict_ch = sorted(dict_res.items(), key=lambda d: d[1], reverse=True)
    return dict_ch[0]


def simple_recommand(movie):
    graph = Graph('http://localhost:7474', auth=('neo4j', '111111'))
    re_movie = recommend(graph, movie)
    return re_movie[0]


if __name__ == '__main__':
    graph = Graph('http://localhost:7474', auth=('neo4j', '111111'))
    f = open(r"..\..\Data\RCdata\movie_similar.csv", "a+", encoding='utf-8', newline='')
    f_csv = csv.writer(f)
    df_movie = pd.DataFrame(graph.run(
        "MATCH (m:Movie) RETURN m.name LIMIT 500"), columns=["m_name"])
    for index, row in df_movie.iterrows():
        name = row["m_name"]
        re_movie = recommend(graph, name)
        print(name + ":" + re_movie[0])
        this_row = [None for _ in range(3)]
        this_row[0] = name
        this_row[1] = re_movie[0]
        this_row[2] = "similar"
        f_csv.writerow(this_row)
    f.close()
