# -*- coding: utf-8 -*-
from Code.TransE.Predict import deep_recommand
from Code.QA.QA import QA
from Code.Recommand.Recommendation import simple_recommand

if __name__ == '__main__':
    print("欢迎来到影视知识图谱服务系统，该系统提供以下服务：")
    print("1-简单电影推荐服务 2-深度电影推荐服务 3-电影知识问答服务")
    print("其中很多服务需要数据库Neo4j的支持，请安装好相应的数据库和数据并开启该系统！")
    print("请选择您想要的服务，输入序号1-3开始服务，输入其他数字结束服务")
    while True:
        num = eval(input())
        if num == 1:
            movie = input("请输入想要进行相似性推荐的电影：")
            movies = simple_recommand(movie)
            print("根据此电影向您推荐《" + movies + "》这部电影。")
        elif num == 2:
            movie = input("请输入想要进行相似性推荐的电影：")
            movies = deep_recommand(movie)
            print("根据此电影向您推荐《" + movies + "》这部电影。")
        elif num == 3:
            QA()
        else:
            break
