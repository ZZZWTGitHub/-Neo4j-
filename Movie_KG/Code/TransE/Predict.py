import codecs
import json
import numpy as np
from Code.TransE.transE import data_loader, entity2id, movie_entity_set


def dataloader(entity_file, relation_file):
    entity_dict = {}
    relation_dict = {}

    with codecs.open(entity_file) as e_f:
        lines = e_f.readlines()
        for line in lines:
            entity, embedding = line.strip().split('\t')
            embedding = np.array(json.loads(embedding))
            entity_dict[int(entity)] = embedding

    with codecs.open(relation_file) as r_f:
        lines = r_f.readlines()
        for line in lines:
            relation, embedding = line.strip().split('\t')
            embedding = np.array(json.loads(embedding))
            relation_dict[int(relation)] = embedding

    return entity_dict, relation_dict


def distance(h, r, t):
    return np.linalg.norm(h + r - t)


def test(id, entity_set, entity_dict, relation_dict):
    rank_dict = {}
    for entity in entity_set:
        h = entity_dict[id]
        r = relation_dict[5]
        t = entity_dict[entity]
        rank = distance(h, r, t)
        rank_dict[entity] = rank
    rank_order = sorted(rank_dict.items(), key=lambda x: x[1], reverse=False)
    return rank_order[0]


def deep_recommand(movie):
    _, _, _ = data_loader()
    id = entity2id[movie]
    movie_entity_set.discard(id)
    entity_dict, relation_dict = dataloader(r"Data\TEdata\entity_50dim_batch400",
                                            r"Data\TEdata\relation_50dim_batch400")
    similar_id = test(id, movie_entity_set, entity_dict, relation_dict)
    for movie in entity2id.keys():
        if entity2id[movie] == similar_id[0]:
            return movie


if __name__ == '__main__':
    _, _, _ = data_loader()
    name = "囚徒"
    id = entity2id[name]
    print(id)
    movie_entity_set.discard(id)
    entity_dict, relation_dict = dataloader(r"..\..\Data\TEdata\entity_50dim_batch400", r"..\..\Data\TEdata\relation_50dim_batch400")
    similar_id = test(id, movie_entity_set, entity_dict, relation_dict)
    print(similar_id)
    for sid in similar_id:
        for movie in entity2id.keys():
            if entity2id[movie] == sid[0]:
                print(movie)
                break
