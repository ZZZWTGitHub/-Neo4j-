import pandas as pd
import re


def main():
    file_name = '..//..//Data//NewKGData//movie.csv'
    old_data = '..//..//Data//PreparedData//movie.csv'
    csv_data = pd.read_csv(file_name, encoding='utf-8', header=None)
    csv_data2 = pd.read_csv(old_data, encoding='utf-8')
    df = pd.DataFrame(csv_data, dtype=str)
    df_ = df.drop_duplicates()
    df_movie = pd.DataFrame(csv_data2, dtype=str)
    film_list = []
    for idx, data in df_movie.iterrows():
        film_list.append(data[1])
    rank_dict = {}
    for idx, data in df_.iterrows():
        film_name = data[0].split(' ')[0]
        if film_name in film_list:
            rank_dict[film_name] = data[1]
    print(rank_dict)
    return rank_dict


if __name__ == '__main__':
    rank = main()
    movie_rank = []
    for film in rank.keys():
        movie_rank.append([film, rank[film]])
    columns = ["movie_name", "rank"]
    df = pd.DataFrame(movie_rank, columns=columns).drop_duplicates()
    df.to_csv(r'..\..\Data\NewKGData\movie_rank.csv', encoding='utf-8', index=False)
