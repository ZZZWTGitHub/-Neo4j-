import codecs
import random
import math
import numpy as np
import pandas as pd
import copy
import time

entity2id = {}
relation2id = {}
movie_entity_set = set()


def data_loader():
    file1 = r"Data\TEdata\train.csv"
    file2 = r"Data\TEdata\entity2id.csv"
    file3 = r"Data\TEdata\relation2id.csv"
    csv_train = pd.read_csv(file1, encoding='utf-8', header=None)
    df_train = pd.DataFrame(csv_train, dtype=str)
    csv_e = pd.read_csv(file2, encoding='utf-8', header=None)
    df_e = pd.DataFrame(csv_e, dtype=str)
    csv_r = pd.read_csv(file3, encoding='utf-8', header=None)
    df_r = pd.DataFrame(csv_r, dtype=str)
    entity_set = set()
    for index, row in df_e.iterrows():
        entity2id[row[1]] = int(row[0])
        entity_set.add(int(row[0]))
        if int(row[0]) > 3318:
            movie_entity_set.add(int(row[0]))
    for index, row in df_r.iterrows():
        relation2id[row[1]] = int(row[0])

    relation_set = set()
    triple_list = []
    for index, row in df_train.iterrows():
        h_ = entity2id[row[0]]
        t_ = entity2id[row[1]]
        r_ = relation2id[row[2]]
        triple_list.append([h_, t_, r_])
        relation_set.add(r_)

    return entity_set, relation_set, triple_list


def distance1(h, r, t):
    return np.sum(np.fabs(h + r - t))


def distance2(h, r, t):
    return np.sum(np.square(h + r - t))


class TransE:
    def __init__(self, entity_set, relation_set, triple_list,
                 embedding_dim=100, learning_rate=0.01, margin=1, l1=True):
        self.embedding_dim = embedding_dim
        self.learning_rate = learning_rate
        self.margin = margin
        self.entity = entity_set
        self.relation = relation_set
        self.triple_list = triple_list
        self.L1 = l1

        self.loss = 0

    def emb_initialize(self):
        relation_dict = {}
        entity_dict = {}

        for relation in self.relation:
            r_emb_temp = np.random.uniform(-6 / math.sqrt(self.embedding_dim),
                                           6 / math.sqrt(self.embedding_dim),
                                           self.embedding_dim)
            relation_dict[relation] = r_emb_temp / np.linalg.norm(r_emb_temp, ord=2)

        for entity in self.entity:
            e_emb_temp = np.random.uniform(-6 / math.sqrt(self.embedding_dim),
                                           6 / math.sqrt(self.embedding_dim),
                                           self.embedding_dim)
            entity_dict[entity] = e_emb_temp / np.linalg.norm(e_emb_temp, ord=2)

        self.relation = relation_dict
        self.entity = entity_dict

    def train(self, epochs):
        nbatches = 40
        batch_size = len(self.triple_list) // nbatches
        print("batch size: ", batch_size)
        for epoch in range(epochs):
            start = time.time()
            self.loss = 0

            for k in range(nbatches):
                sbatch = random.sample(self.triple_list, batch_size)
                tbatch = []
                for triple in sbatch:
                    corrupted_triple = self.corrupt(triple)
                    tbatch.append((triple, corrupted_triple))
                self.update_embeddings(tbatch)

            end = time.time()
            print("epoch: ", epoch, "cost time: %s" % (round((end - start), 3)))
            print("loss: ", self.loss)

            if epoch % 10 == 0:
                with codecs.open("entity_temp", "w") as f_e:
                    for e in self.entity.keys():
                        f_e.write(str(e) + "\t")
                        f_e.write(str(list(self.entity[e])))
                        f_e.write("\n")
                with codecs.open("relation_temp", "w") as f_r:
                    for r in self.relation.keys():
                        f_r.write(str(r) + "\t")
                        f_r.write(str(list(self.relation[r])))
                        f_r.write("\n")
                with codecs.open("result_temp", "a") as f_s:
                    f_s.write("epoch: %d\tloss: %s\n" % (epoch, self.loss))

        print("写入文件...")
        with codecs.open("entity_50dim_batch400", "w") as f1:
            for e in self.entity.keys():
                f1.write(str(e) + "\t")
                f1.write(str(list(self.entity[e])))
                f1.write("\n")

        with codecs.open("relation_50dim_batch400", "w") as f2:
            for r in self.relation.keys():
                f2.write(str(r) + "\t")
                f2.write(str(list(self.relation[r])))
                f2.write("\n")
        print("写入完成")

    def corrupt(self, triple):
        corrupted_triple = copy.deepcopy(triple)
        seed = random.random()
        if seed > 0.5:
            head = triple[0]
            rand_head = head
            while rand_head == head:
                rand_head = random.randint(0, len(self.entity) - 1)
            corrupted_triple[0] = rand_head
        else:

            tail = triple[0]
            rand_tail = tail
            while rand_tail == tail:
                rand_tail = random.randint(0, len(self.entity) - 1)
            corrupted_triple[1] = rand_tail
        return corrupted_triple

    def update_embeddings(self, tbatch):
        entity_updated = {}
        relation_updated = {}
        for triple, corrupted_triple in tbatch:
            h_correct = self.entity[triple[0]]
            t_correct = self.entity[triple[1]]
            relation = self.relation[triple[2]]
            h_corrupt = self.entity[corrupted_triple[0]]
            t_corrupt = self.entity[corrupted_triple[1]]

            if triple[0] in entity_updated.keys():
                pass
            else:
                entity_updated[triple[0]] = copy.copy(self.entity[triple[0]])
            if triple[1] in entity_updated.keys():
                pass
            else:
                entity_updated[triple[1]] = copy.copy(self.entity[triple[1]])
            if triple[2] in relation_updated.keys():
                pass
            else:
                relation_updated[triple[2]] = copy.copy(self.relation[triple[2]])
            if corrupted_triple[0] in entity_updated.keys():
                pass
            else:
                entity_updated[corrupted_triple[0]] = copy.copy(self.entity[corrupted_triple[0]])
            if corrupted_triple[1] in entity_updated.keys():
                pass
            else:
                entity_updated[corrupted_triple[1]] = copy.copy(self.entity[corrupted_triple[1]])

            if self.L1:
                dist_correct = distance1(h_correct, relation, t_correct)
                dist_corrupt = distance1(h_corrupt, relation, t_corrupt)
            else:
                dist_correct = distance2(h_correct, relation, t_correct)
                dist_corrupt = distance2(h_corrupt, relation, t_corrupt)

            err = self.hinge_loss(dist_correct, dist_corrupt)

            if err > 0:
                self.loss += err
                grad_pos = 2 * (h_correct + relation - t_correct)
                grad_neg = 2 * (h_corrupt + relation - t_corrupt)
                if self.L1:
                    for i in range(len(grad_pos)):
                        if grad_pos[i] > 0:
                            grad_pos[i] = 1
                        else:
                            grad_pos[i] = -1

                    for i in range(len(grad_neg)):
                        if grad_neg[i] > 0:
                            grad_neg[i] = 1
                        else:
                            grad_neg[i] = -1

                entity_updated[triple[0]] -= self.learning_rate * grad_pos
                entity_updated[triple[1]] -= (-1) * self.learning_rate * grad_pos

                entity_updated[corrupted_triple[0]] -= (-1) * self.learning_rate * grad_neg
                entity_updated[corrupted_triple[1]] -= self.learning_rate * grad_neg

                relation_updated[triple[2]] -= self.learning_rate * grad_pos
                relation_updated[triple[2]] -= (-1) * self.learning_rate * grad_neg

        for i in entity_updated.keys():
            entity_updated[i] /= np.linalg.norm(entity_updated[i])
            self.entity[i] = entity_updated[i]
        for i in relation_updated.keys():
            relation_updated[i] /= np.linalg.norm(relation_updated[i])
            self.relation[i] = relation_updated[i]
        return

    def hinge_loss(self, dist_correct, dist_corrupt):
        return max(0, dist_correct - dist_corrupt + self.margin)


if __name__ == '__main__':
    entity_set, relation_set, triple_list = data_loader()

    print("load file...")
    print("Complete load. entity : %d , relation : %d , triple : %d" % (
        len(entity_set), len(relation_set), len(triple_list)))

    transE = TransE(entity_set, relation_set, triple_list, embedding_dim=3, learning_rate=0.01, margin=1, l1=False)
    transE.emb_initialize()
    transE.train(epochs=400)
