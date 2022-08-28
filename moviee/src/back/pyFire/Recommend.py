import codecs
import json
import string
import numpy as np
import pandas as pd
import sys

entity2id = {}
movie_entity_set = set()


def data_loader():
    # file = r'entity2id.csv'#读入实体名称和序号的对应关系，如肖申克的救赎对应编号40856
    file = r'E:\\2022-1term\\大数据特色课程模块\\HW\Website-for-Knowledge-Graph-Inference\\moviee\\src\\back\\pyFire\\entity2id.csv'
    csv_e = pd.read_csv(file, encoding='utf-8', header=None)
    df_e = pd.DataFrame(csv_e, dtype=str)

    for index, row in df_e.iterrows():
        entity2id[row[1]] = int(row[0])#存储实体名称和序号的对应关系，{肖申克的救赎,40856}
        if int(row[0]) > 40855:
            movie_entity_set.add(int(row[0]))#存储是电影的序号，实体编号从40856开始是电影，之前是类型之类的
    return


def dataloader(entity_file):
    entity_dict = {}#存储实体名称和向量的对应关系，{40856,[-0.05322420585356012, 0.025689128051673775, 0.07914839244860701, -0.09883326899752927, 0.058403944919611615, -0.07383247604790864, 0.015097391058518267, -0.06432854166192357, 0.0444697774588407, 0.008065020969093483, 0.19136404992710446, -0.095635614078616, -0.16914794187841797, 0.15832979417456744, -0.012469331219384486, 0.1302714200804788, -0.3006372538579072, -0.40142964655423546, 0.16612412061924017, -0.21608366903165885, -0.0341882489747573, 0.003282002004819439, -0.15863287702143117, -0.06109727155343185, -0.04652362308123718, -0.05037917593542324, -0.031256727404834324, -0.05041893605152852, 0.08383171365177085, 0.028982320754571748, -0.18448428861387328, -0.11256171850914419, -0.13008665847051845, 0.09967381632551672, 0.044766465620051994, 0.1407510639389346, -0.2981006291526377, 0.10251121924256057, -0.004344683989619165, -0.1099624951372856, 0.18289797898570467, 0.01316448078570744, -0.21928647375368673, 0.12894891639273975, -0.050676103585796745, -0.03414216973305491, -0.34624334322116435, 0.0785768455584906, -0.19429517734605126, -0.06249276869669911]}
                    #即用该向量代表肖申克的救赎这部电影
    with codecs.open(entity_file) as e_f:
        lines = e_f.readlines()#就是读文件操作
        for line in lines:
            entity, embedding = line.strip().split('\t')#中间用空格划分的序号和向量
            embedding = np.array(json.loads(embedding))#转化成python数组格式
            entity_dict[int(entity)] = embedding

    return entity_dict


def distance(h, t):
    return np.linalg.norm(h - t)#就是求距离的那个公式，例如向量(x1,y1)和(x2,y2)，返回(x1-y1)的平方+(x2-y2)的平方，开不开方无所谓


def test(id, entity_set, entity_dict):
    rank_dict = {}
    for entity in entity_set:#在所有其他电影里寻找和所推荐电影向量距离最小的
        h = entity_dict[id]#这是要推荐的电影的向量
        t = entity_dict[entity]#这是其他电影的向量
        rank = distance(h, t)#得到对应的值
        rank_dict[entity] = rank#记录在字典里
    rank_order = sorted(rank_dict.items(), key=lambda x: x[1], reverse=False)#排个序找到最小的那个
    return rank_order[0]

def maincode(argv):
    # print(argv)
    data_loader()
    name = str(argv[0])
    id = entity2id[name]    # 获得电影对应序号
    movie_entity_set.discard(id)    # 在所有电影中去除推荐电影本身
    entity_dict = dataloader(r"E:\\2022-1term\\大数据特色课程模块\\HW\Website-for-Knowledge-Graph-Inference\\moviee\\src\\back\\pyFire\\entity_50dim_batch252")#导入向量数据的文件
    similar_id = test(id, movie_entity_set, entity_dict)#找相似的电影
    for movie in entity2id.keys():  # 遍历一下电影名称和id的字典将电影名称输出
        if entity2id[movie] == similar_id[0]:
            # print(similar_id[0] - 40856)
            print(movie)
            break

if __name__ == '__main__':
    maincode(sys.argv[1:])
