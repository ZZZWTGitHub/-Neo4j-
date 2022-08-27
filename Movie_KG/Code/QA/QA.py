# -*- coding: utf-8 -*-
import jieba
import jieba.posseg
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from py2neo import Graph


class QuestionTemplate:
    global graph
    graph = Graph('http://localhost:7474', auth=('neo4j', '111111'))

    def __init__(self):
        self.raw_question = None
        self.question_flag = None
        self.question_word = None
        self.template_str2list = None
        self.template_id = None
        self.q_template_dict = {
            0: self.get_movie_releaseyear,
            1: self.get_movie_type,
            2: self.get_movie_actor_list,
            3: self.get_actor_act_type_movie,
            4: self.get_actor_act_movie_list,
            5: self.get_actor_movie_type,
            6: self.get_cooperation_movie_list,
            7: self.get_actor_movie_num,
        }

    def get_question_answer(self, question, template):
        template_id, template_str = int(template.split("\t")[0]), template.split("\t")[1]
        self.template_id = template_id
        self.template_str2list = template_str.split()

        question_word, question_flag = [], []
        for q in question:
            word, flag = q.split("/")
            question_word.append(word)
            question_flag.append(flag)
        self.question_word = question_word
        self.question_flag = question_flag
        self.raw_question = question
        answer = self.q_template_dict[template_id]()
        return answer

    def get_movie_name(self):
        tag_index = self.question_flag.index("nm")
        movie_name = self.question_word[tag_index]
        return movie_name

    def get_name(self, type_str):
        name_count = self.question_flag.count(type_str)
        if name_count == 1:
            tag_index = self.question_flag.index(type_str)
            name = self.question_word[tag_index]
            return name
        else:
            result_list = []
            for i, flag in enumerate(self.question_flag):
                if flag == type_str:
                    result_list.append(self.question_word[i])
            return result_list

    def get_movie_releaseyear(self):
        movie_name = self.get_movie_name()
        cql = f"match(m:Movie) where m.name='{movie_name}' return m.year"
        answer = list(graph.run(cql))[0]
        final_answer = movie_name + "的上映时间是" + str(answer) + "年。"
        return final_answer

    def get_movie_type(self):
        movie_name = self.get_movie_name()
        cql = f"match(m:Movie)-[]-(n:Type) where m.name='{movie_name}' return n.name"
        answer = pd.DataFrame(graph.run(cql), columns=['type'])
        answer_list = list(answer['type'])
        answer = "、".join(answer_list)
        final_answer = movie_name + "是" + str(answer) + "等类型的电影。"
        return final_answer

    def get_movie_actor_list(self):
        movie_name = self.get_movie_name()
        cql = f"match(n:Actor)-[]-(m:Movie) where m.name='{movie_name}' return n.name"
        answer = pd.DataFrame(graph.run(cql), columns=['name'])
        answer_list = list(answer['name'])
        answer = "、".join(answer_list)
        final_answer = movie_name + "由" + str(answer) + "等演员主演。"
        return final_answer

    def get_actor_act_type_movie(self):
        actor_name = self.get_name("nr")
        type = self.get_name("ng")
        movie_name_list = self.get_actorname_movie_list(actor_name)
        result = []
        for movie_name in movie_name_list:
            try:
                cql = f"match(m:Movie)-[]-(t:Type) where m.name='{movie_name}' return t.name"
                get_type = pd.DataFrame(graph.run(cql), columns=['type'])
                type_list = list(get_type['type'])
                if len(type_list) == 0:
                    continue
                if type in type_list:
                    result.append(movie_name)
            except:
                continue
        answer = "、".join(result)
        final_answer = str(actor_name) + "演过的" + type + "类型的电影有:\n" + answer
        return final_answer

    def get_actor_act_movie_list(self):
        actor_name = self.get_name("nr")
        answer_list = self.get_actorname_movie_list(actor_name)
        answer = "、".join(answer_list)
        final_answer = str(actor_name) + "演过的电影有:\n" + str(answer)
        return final_answer

    def get_actorname_movie_list(self, actorname):
        cql = f"match(n:Actor)-[]-(m:Movie) where n.name='{actorname}' return m.name"
        answer = pd.DataFrame(graph.run(cql), columns=['movie'])
        answer_list = list(answer['movie'])
        return answer_list

    def get_actor_movie_type(self):
        actor_name = self.get_name("nr")
        movie_name_list = self.get_actorname_movie_list(actor_name)
        result = []
        for movie_name in movie_name_list:
            movie_name = str(movie_name).strip()
            try:
                cql = f"match(m:Movie)-[]-(t:Type) where m.name='{movie_name}' return t.name"
                get_type = pd.DataFrame(graph.run(cql), columns=['type']).drop_duplicates()
                type_list = list(get_type['type'])
                if len(type_list) == 0:
                    continue
                result.extend(type_list)
            except:
                continue
        answer = "、".join(list(set(result)))
        final_answer = str(actor_name) + "演过的电影类型有" + answer + "等。"
        return final_answer

    def get_cooperation_movie_list(self):
        actor_name_list = self.get_name('nr')
        movie_list = {}
        for i, actor_name in enumerate(actor_name_list):
            answer_list = self.get_actorname_movie_list(actor_name)
            movie_list[i] = answer_list
        result_list = list(set(movie_list[0]).intersection(set(movie_list[1])))
        answer = "、".join(result_list)
        final_answer = actor_name_list[0] + "和" + actor_name_list[1] + "一起演过的电影主要有" + answer
        return final_answer

    def get_actor_movie_num(self):
        actor_name = self.get_name("nr")
        answer_list = self.get_actorname_movie_list(actor_name)
        movie_num = len(set(answer_list))
        answer = movie_num
        final_answer = str(actor_name) + "演过" + str(answer) + "部电影。"
        return final_answer


class Question:
    def __init__(self):
        self.question_flag = None
        self.question_word = None
        self.answer = None
        self.question_template_id_str = None
        self.pos_quesiton = None
        self.raw_question = None
        self.question_template = None
        self.question_mode_dict = None
        self.classify_model = None
        self.create_class_type()

    def create_class_type(self):
        self.classify_model = QuestionPrediction()
        with(open(r"Data\QAdata\question_classification.txt", "r", encoding="utf-8")) as f:
            question_mode_list = f.readlines()
        self.question_mode_dict = {}
        for one_mode in question_mode_list:
            mode_id, mode_str = one_mode.strip().split(":")
            self.question_mode_dict[int(mode_id)] = mode_str.strip()
        self.question_template = QuestionTemplate()

    def question_process(self, question):
        self.raw_question = question.strip()
        self.pos_quesiton = self.question_posseg()
        self.question_template_id_str = self.get_question_template()
        self.answer = self.query_template()
        return self.answer

    def question_posseg(self):
        jieba.load_userdict(r"Data\QAdata\userdict.txt")
        clean_question = re.sub("[+.!/_,$%^*(\"\')]+|[+—()?【】“”！，。？、~@#￥%…&*（）]+", "", self.raw_question)
        question_seged = jieba.posseg.cut(clean_question)
        result = []
        question_word, question_flag = [], []
        for w in question_seged:
            temp_word = f"{w.word}/{w.flag}"
            result.append(temp_word)
            word, flag = w.word, w.flag
            question_word.append(word.strip())
            question_flag.append(flag.strip())
        self.question_word = question_word
        self.question_flag = question_flag
        return result

    def get_question_template(self):
        for item in ['nr', 'nm', 'ng']:
            while item in self.question_flag:
                ix = self.question_flag.index(item)
                self.question_word[ix] = item
                self.question_flag[ix] = item + "ed"
        str_question = "".join(self.question_word)
        question_template_num = self.classify_model.predict(str_question)
        question_template = self.question_mode_dict[question_template_num]
        question_template_id_str = str(question_template_num) + "\t" + question_template
        return question_template_id_str

    def query_template(self):
        try:
            answer = self.question_template.get_question_answer(self.pos_quesiton, self.question_template_id_str)
        except:
            answer = "真抱歉，我也不知道问题的答案！"
        return answer


class QuestionPrediction:

    def __init__(self):
        self.tv = None
        self.train_file = r"Data\QAdata\train.csv"
        self.train_x, self.train_y = self.read_train_data(self.train_file)
        self.model = self.train_model_NB()

    def read_train_data(self, template_train_file):
        train_data = pd.read_csv(template_train_file, encoding='utf-8')
        train_x = train_data["text"].apply(lambda x: " ".join(list(jieba.cut(str(x))))).tolist()
        train_y = train_data["label"].tolist()
        return train_x, train_y

    def train_model_NB(self):
        x_train, y_train = self.train_x, self.train_y
        self.tv = TfidfVectorizer()
        train_data = self.tv.fit_transform(x_train).toarray()
        clf = MultinomialNB(alpha=0.01)
        clf.fit(train_data, y_train)
        return clf

    def predict(self, question):
        question = [" ".join(list(jieba.cut(question)))]
        test_data = self.tv.transform(question).toarray()
        y_pred = self.model.predict(test_data)[0]
        return y_pred


def QA():
    question = Question()
    ask = input("请输入你的问题：")
    answer = question.question_process(ask)
    print(answer)


if __name__ == '__main__':
    question = Question()
    ask = input("请输入您的问题：")
    answer = question.question_process(ask)
    print(answer)
