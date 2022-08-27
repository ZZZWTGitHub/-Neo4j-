from py2neo import Graph
import pandas as pd
if __name__ == '__main__':
    graph = Graph('http://localhost:7474', auth=('neo4j', '111111'))

    cql = f"match(m:Movie) return m.name"
    movie = pd.DataFrame(graph.run(cql), columns=['movie'])
    movie_list = list(movie['movie'])
    for m in movie_list:
        str = m+" 15"+" nm\n"
        f = open(r'..\..\Data\QAdata\userdict.txt', 'a+', encoding='utf-8')
        f.writelines(str)

    cql = f"match(n:Actor) return n.name"
    actor = pd.DataFrame(graph.run(cql), columns=['actor'])
    actor_list = list(actor['actor'])
    for a in actor_list:
        str = a + " 15" + " nr\n"
        f = open(r'..\..\Data\QAdata\userdict.txt', 'a+', encoding='utf-8')
        f.writelines(str)

    cql = f"match(n:Type) return n.name"
    type = pd.DataFrame(graph.run(cql), columns=['type'])
    type_list = list(type['type'])
    for t in type_list:
        str = t + " 15" + " ng\n"
        f = open(r'..\..\Data\QAdata\userdict.txt', 'a+', encoding='utf-8')
        f.writelines(str)
