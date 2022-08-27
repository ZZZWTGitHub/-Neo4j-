from py2neo import Graph
import pandas as pd

if __name__ == '__main__':
    graph = Graph('http://localhost:7474', auth=('neo4j', '111111'))
    df_movie = pd.DataFrame(
        graph.run("MATCH (m:Movie) RETURN m.name LIMIT 800"),
        columns=["e_name"])
    
    df_t = pd.DataFrame(
        graph.run("MATCH p=(m:Movie)-[r:movie_type]-(n:Type) RETURN m.name,n.name,r.label LIMIT 1000"),
        columns=["e1_name", "e2_name", "r_name"])
    df_a = pd.DataFrame(
        graph.run("MATCH p=(m:Movie)-[r:movie_actor]-(n:Actor) RETURN m.name,n.name,r.label LIMIT 2000"),
        columns=["e1_name", "e2_name", "r_name"])
    df_d = pd.DataFrame(
        graph.run("MATCH p=(m:Movie)-[r:movie_director]-(n:Director) RETURN m.name,n.name,r.label LIMIT 1000"),
        columns=["e1_name", "e2_name", "r_name"])
    df_s = pd.DataFrame(
        graph.run("MATCH p=(m:Movie)-[r:movie_scriptwriter]-(n:Scriptwriter) RETURN m.name,n.name,r.label LIMIT 2000"),
        columns=["e1_name", "e2_name", "r_name"])
    df_c = pd.DataFrame(
        graph.run("MATCH p=(m:Movie)-[r:movie_country]-(n:Country) RETURN m.name,n.name,r.label LIMIT 500"),
        columns=["e1_name", "e2_name", "r_name"])

    df = pd.concat([df_t, df_a, df_d, df_s, df_c])
    df.reset_index(drop=True, inplace=True)
    print(df)
    df.to_csv(r'..\..\Data\TEdata\train.csv', index=False, header=False)

    df_e2 = pd.DataFrame(df["e2_name"])
    df_e2.rename(columns={"e2_name": "e_name"}, inplace=True)
    df_movie = pd.DataFrame(
        graph.run("MATCH (m:Movie) RETURN m.name"),
        columns=["e_name"])
    df_e = pd.concat([df_e2, df_movie]).drop_duplicates(subset=["e_name"])
    df_e.reset_index(drop=True, inplace=True)
    print(df_e)
    df_e.to_csv(r'..\..\Data\TEdata\entity2id.csv', index=True, header=False)

    df_r = pd.DataFrame(df["r_name"]).drop_duplicates(subset=["r_name"])
    df_r.reset_index(drop=True, inplace=True)
    print(df_r)
    df_r.to_csv(r'..\..\Data\TEdata\relation2id.csv', index=True, header=False)
