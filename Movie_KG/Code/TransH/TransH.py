import codecs
import numpy as np
import copy
import time
import random
import pandas as pd

entity2id = {}
relation2id = {}
relation_tph = {}
relation_hpt = {}


def data_loader():
    file1 = r'..\..\Data\THdata\train.csv'
    file2 = r'..\..\Data\THdata\entity2id.csv'
    file3 = r'..\..\Data\THdata\relation2id.csv'

    csv_train = pd.read_csv(file1, encoding='utf-8', header=None)
    df_train = pd.DataFrame(csv_train, dtype=str)
    csv_e = pd.read_csv(file2, encoding='utf-8', header=None)
    df_e = pd.DataFrame(csv_e, dtype=str)
    csv_r = pd.read_csv(file3, encoding='utf-8', header=None)
    df_r = pd.DataFrame(csv_r, dtype=str)

    for index, row in df_e.iterrows():
        entity2id[row[1]] = int(row[0])

    for index, row in df_r.iterrows():
        relation2id[row[1]] = int(row[0])

    entity_set = set()
    relation_set = set()
    triple_list = []
    relation_head = {}
    relation_tail = {}

    for index, row in df_train.iterrows():
        h_ = entity2id[row[0]]
        t_ = entity2id[row[1]]
        r_ = relation2id[row[2]]
        triple_list.append([h_, t_, r_])
        entity_set.add(h_)
        entity_set.add(t_)
        relation_set.add(r_)

        if r_ in relation_head:
            if h_ in relation_head[r_]:
                relation_head[r_][h_] += 1
            else:
                relation_head[r_][h_] = 1
        else:
            relation_head[r_] = {}
            relation_head[r_][h_] = 1

        if r_ in relation_tail:
            if t_ in relation_tail[r_]:
                relation_tail[r_][t_] += 1
            else:
                relation_tail[r_][t_] = 1
        else:
            relation_tail[r_] = {}
            relation_tail[r_][t_] = 1

    for r_ in relation_head:
        sum1, sum2 = 0, 0
        for head in relation_head[r_]:
            sum1 += 1
            sum2 += relation_head[r_][head]
        tph = sum2 / sum1
        relation_tph[r_] = tph

    for r_ in relation_tail:
        sum1, sum2 = 0, 0
        for tail in relation_tail[r_]:
            sum1 += 1
            sum2 += relation_tail[r_][tail]
        hpt = sum2 / sum1
        relation_hpt[r_] = hpt

    return entity_set, relation_set, triple_list


def norm_l1(h, r, t):
    return np.sum(np.fabs(h + r - t))


class TransH:
    def __init__(self, entity_set, relation_set, triple_list, embedding_dim=50, lr=0.01, margin=1.0, norm=1, C=1.0,
                 epsilon=1e-5):
        self.entities = entity_set
        self.relations = relation_set
        self.triples = triple_list
        self.dimension = embedding_dim
        self.learning_rate = lr
        self.margin = margin
        self.norm = norm
        self.loss = 0.0
        self.norm_relations = {}
        self.hyper_relations = {}
        self.C = C
        self.epsilon = epsilon

    def data_initialise(self):
        entityVectorList = {}
        relationNormVectorList = {}
        relationHyperVectorList = {}
        for entity in self.entities:
            entity_vector = np.random.uniform(-6.0 / np.sqrt(self.dimension), 6.0 / np.sqrt(self.dimension),
                                              self.dimension)
            entityVectorList[entity] = entity_vector

        for relation in self.relations:
            relation_norm_vector = np.random.uniform(-6.0 / np.sqrt(self.dimension), 6.0 / np.sqrt(self.dimension),
                                                     self.dimension)
            relation_hyper_vector = np.random.uniform(-6.0 / np.sqrt(self.dimension), 6.0 / np.sqrt(self.dimension),
                                                      self.dimension)
            relation_norm_vector = self.normalization(relation_norm_vector)
            relation_hyper_vector = self.normalization(relation_hyper_vector)
            relationNormVectorList[relation] = relation_norm_vector
            relationHyperVectorList[relation] = relation_hyper_vector

        self.entities = entityVectorList
        self.norm_relations = relationNormVectorList
        self.hyper_relations = relationHyperVectorList

    def training_run(self, epochs=100, nbatches=400):

        batch_size = int(len(self.triples) / nbatches)
        print("batch size: ", batch_size)
        for epoch in range(epochs):
            start = time.time()
            self.loss = 0.0
            # Normalise the embedding of the entities to 1
            for entity in self.entities:
                self.entities[entity] = self.normalization(self.entities[entity])

            for batch in range(nbatches):
                batch_samples = random.sample(self.triples, batch_size)

                Tbatch = []
                for sample in batch_samples:
                    corrupted_sample = copy.deepcopy(sample)
                    pr = np.random.random(1)[0]
                    p = relation_tph[corrupted_sample[2]] / (
                            relation_tph[corrupted_sample[2]] + relation_hpt[corrupted_sample[2]])

                    if pr < p:
                        # change the head entity
                        corrupted_sample[0] = random.sample(self.entities.keys(), 1)[0]
                        while corrupted_sample[0] == sample[0]:
                            corrupted_sample[0] = random.sample(self.entities.keys(), 1)[0]
                    else:
                        # change the tail entity
                        corrupted_sample[1] = random.sample(self.entities.keys(), 1)[0]
                        while corrupted_sample[1] == sample[1]:
                            corrupted_sample[1] = random.sample(self.entities.keys(), 1)[0]

                    if (sample, corrupted_sample) not in Tbatch:
                        Tbatch.append((sample, corrupted_sample))

                self.update_triple_embedding(Tbatch)
            end = time.time()
            print("epoch: ", epoch, "cost time: %s" % (round((end - start), 3)))
            print("running loss: ", self.loss)

            with codecs.open("entity_" + str(self.dimension) + "dim_batch" + str(batch_size), "w") as f1:
                for e in self.entities:
                    f1.write(str(e) + "\t")
                    f1.write(str(list(self.entities[e])))
                    f1.write("\n")

            with codecs.open("relation_norm_" + str(self.dimension) + "dim_batch" + str(batch_size), "w") as f2:
                for r in self.norm_relations:
                    f2.write(str(r) + "\t")
                    f2.write(str(list(self.norm_relations[r])))
                    f2.write("\n")

            with codecs.open("relation_hyper_" + str(self.dimension) + "dim_batch" + str(batch_size), "w") as f3:
                for r in self.hyper_relations:
                    f3.write(str(r) + "\t")
                    f3.write(str(list(self.hyper_relations[r])))
                    f3.write("\n")

        '''with codecs.open("entity_" + str(self.dimension) + "dim_batch" + str(batch_size), "w") as f1:

            for e in self.entities:
                f1.write(str(e) + "\t")
                
                f1.write(str(list(self.entities[e])))
                f1.write("\n")

        with codecs.open("relation_norm_" + str(self.dimension) + "dim_batch" + str(batch_size), "w") as f2:
            for r in self.norm_relations:
                f2.write(r + "\t")
                f2.write(str(list(self.norm_relations[r])))
                f2.write("\n")

        with codecs.open("relation_hyper_" + str(self.dimension) + "dim_batch" + str(batch_size), "w") as f3:
            for r in self.hyper_relations:
                f3.write(r + "\t")
                f3.write(str(list(self.hyper_relations[r])))
                f3.write("\n")'''

    def normalization(self, vector):
        return vector / np.linalg.norm(vector)

    def norm_l2(self, h, r_norm, r_hyper, t):
        return np.sum(np.square(h - np.dot(r_norm, h) * r_norm + r_hyper - t + np.dot(r_norm, t) * r_norm))

    def scale_entity(self, h, t, h_c, t_c):
        return np.linalg.norm(h) ** 2 - 1 + np.linalg.norm(t) ** 2 - 1 + np.linalg.norm(h_c) ** 2 - 1 + np.linalg.norm(
            t_c) ** 2 - 1

    def orthogonality(self, norm, hyper):
        return np.dot(norm, hyper) ** 2 / np.linalg.norm(hyper) ** 2 - self.epsilon ** 2

    def update_triple_embedding(self, Tbatch):
        copy_entity = copy.deepcopy(self.entities)
        copy_norm_relation = copy.deepcopy(self.norm_relations)
        copy_hyper_relation = copy.deepcopy(self.hyper_relations)

        for correct_sample, corrupted_sample in Tbatch:

            correct_copy_head = copy_entity[correct_sample[0]]
            correct_copy_tail = copy_entity[correct_sample[1]]
            relation_norm_copy = copy_norm_relation[correct_sample[2]]
            relation_hyper_copy = copy_hyper_relation[correct_sample[2]]

            corrupted_copy_head = copy_entity[corrupted_sample[0]]
            corrupted_copy_tail = copy_entity[corrupted_sample[1]]

            correct_head = self.entities[correct_sample[0]]
            correct_tail = self.entities[correct_sample[1]]
            relation_norm = self.norm_relations[correct_sample[2]]
            relation_hyper = self.hyper_relations[correct_sample[2]]

            corrupted_head = self.entities[corrupted_sample[0]]
            corrupted_tail = self.entities[corrupted_sample[1]]

            # calculate the distance of the triples
            correct_distance = self.norm_l2(correct_head, relation_norm, relation_hyper, correct_tail)
            corrupted_distance = self.norm_l2(corrupted_head, relation_norm, relation_hyper, corrupted_tail)

            loss = self.margin + correct_distance - corrupted_distance
            loss1 = self.scale_entity(correct_head, correct_tail, corrupted_head, corrupted_tail)
            # loss2 = self.orthogonality(relation_norm, relation_hyper)

            if loss > 0:
                self.loss += loss
                i = np.ones(self.dimension)
                correct_gradient = 2 * (correct_head - np.dot(relation_norm, correct_head) * relation_norm +
                                        relation_hyper - correct_tail +
                                        np.dot(relation_norm, correct_tail) *
                                        relation_norm) * (i - relation_norm ** 2)
                corrupted_gradient = 2 * (corrupted_head - np.dot(relation_norm, corrupted_head) * relation_norm +
                                          relation_hyper - corrupted_tail +
                                          np.dot(relation_norm, corrupted_tail) *
                                          relation_norm) * (i - relation_norm ** 2)
                hyper_gradient = 2 * (correct_head - np.dot(relation_norm, correct_head) * relation_norm +
                                      - correct_tail + np.dot(relation_norm, correct_tail)
                                      * relation_norm) - 2 * (
                                         corrupted_head - np.dot(relation_norm, corrupted_head) * relation_norm +
                                         - corrupted_tail +
                                         np.dot(relation_norm, corrupted_tail) *
                                         relation_norm)
                norm_gradient = 2 * (correct_head - np.dot(relation_norm, correct_head) * relation_norm +
                                     relation_hyper - correct_tail +
                                     np.dot(relation_norm, correct_tail) *
                                     relation_norm) * (correct_tail - correct_head) * 2 * relation_norm - 2 * (
                                        corrupted_head - np.dot(relation_norm, corrupted_head) * relation_norm +
                                        relation_hyper - corrupted_tail +
                                        np.dot(relation_norm, corrupted_tail) *
                                        relation_norm) * (corrupted_tail - corrupted_head) * 2 * relation_norm

                correct_copy_head -= self.learning_rate * correct_gradient
                relation_norm_copy -= self.learning_rate * norm_gradient
                relation_hyper_copy -= self.learning_rate * hyper_gradient
                correct_copy_tail -= -1 * self.learning_rate * correct_gradient

                if correct_sample[0] == corrupted_sample[0]:
                    # if corrupted_triples replaces the tail entity, the head entity's embedding need to be updated twice
                    correct_copy_head -= -1 * self.learning_rate * corrupted_gradient
                    corrupted_copy_tail -= self.learning_rate * corrupted_gradient
                elif correct_sample[1] == corrupted_sample[1]:
                    # if corrupted_triples replaces the head entity, the tail entity's embedding need to be updated twice
                    corrupted_copy_head -= -1 * self.learning_rate * corrupted_gradient
                    correct_copy_tail -= self.learning_rate * corrupted_gradient

                # normalising these new embedding vector, instead of normalising all the embedding together
                copy_entity[correct_sample[0]] = self.normalization(correct_copy_head)
                copy_entity[correct_sample[1]] = self.normalization(correct_copy_tail)
                if correct_sample[0] == corrupted_sample[0]:
                    # if corrupted_triples replace the tail entity, update the tail entity's embedding
                    copy_entity[corrupted_sample[1]] = self.normalization(corrupted_copy_tail)
                elif correct_sample[1] == corrupted_sample[1]:
                    # if corrupted_triples replace the head entity, update the head entity's embedding
                    copy_entity[corrupted_sample[0]] = self.normalization(corrupted_copy_head)
                # the paper mention that the relation's embedding don't need to be normalised
                copy_norm_relation[correct_sample[2]] = self.normalization(relation_norm_copy)
                copy_hyper_relation[correct_sample[2]] = relation_hyper_copy

        self.entities = copy_entity
        self.norm_relations = copy_norm_relation
        self.hyper_relations = copy_hyper_relation


if __name__ == '__main__':
    entity_set, relation_set, triple_list = data_loader()

    transH = TransH(entity_set, relation_set, triple_list, embedding_dim=50, lr=0.01, margin=1.0, norm=1)
    transH.data_initialise()
    transH.training_run()
