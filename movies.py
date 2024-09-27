import csv
import sys
from collections import defaultdict
import time
import random

class Movie:
    def __init__(self, title : str, genre : str, year : int):     
        self.title = title
        self.genre = genre
        self.year = year

movie_list = [] # list of movie objects, assuming id=index
year_dic = defaultdict(lambda: defaultdict(list))  # dictionary of dictionary of list
unique_years = []
unique_genres = []


def load():
    col_title = 1
    col_genre = 2
    col_year = 6
    with open("IMDB-Movie-Data.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        for i,row in enumerate(reader):
            if i == 0:            
                col_title = row.index('Title')
                col_genre = row.index('Genre')
                col_year = row.index('Year')
            else:
                #print (row)
                title = row[col_title]
                genre = row[col_genre]
                year = int(row[col_year])
                id = i-1
                #print(f' id: {id}, title: {title} genre: {genre} year: {year}')

                movie_list.append(Movie(title, genre, year))

                genres = genre.split(',')
                for genre in genres:
                    year_dic[year][genre.casefold()].append(id)

    global unique_years
    unique_years = sorted(set(year_dic.keys()))

    global unique_genres
    unique_genres = set()
    for genre_dic in year_dic.values():
        unique_genres.update(genre_dic.keys())
    unique_genres = sorted(unique_genres)

    print(unique_years)
    print(unique_genres)

load()


def get_uniques(genre: str = '', year_from: int = 0, year_to: int = 3000):
    if genre != '' and genre.casefold() not in unique_genres:
        raise Exception('invalid genre')

    ids = set()
           
    year_filter = list(set(year_dic.keys()).intersection(range(year_from, year_to+1)))

    for y in year_filter:            
        genre_dic = year_dic[y]
        if genre == '':
            ids.update(genre_dic.values())
        else:
            if genre in genre_dic.keys():
                ids.update(genre_dic[genre.casefold()])
        
    return [movie_list[id].title for id in ids]


# retrieve movies in genre 'Animation', any date
res = get_uniques('animation')
print('### animation, any date ###')
print(res)

# retrieve movies in genre 'Action', 2006-2007
res = get_uniques('action', 2006, 2007)
print('### action, 2006-2007 ##')
print(res)

# test average retrieval time over 1000 random queries
trials = 1000
total_ms = 0
for i in range(0,trials):
    genre = random.choice(unique_genres)
    from_year = random.choice(unique_years)
    to_year = random.choice([y for y in unique_years if y >= from_year])

    tic = time.perf_counter()
    res = get_uniques(genre, from_year, to_year)
    toc = time.perf_counter()
    ms = (toc - tic) * 1000
    total_ms += ms
avg_ms = total_ms / trials
print(f'{avg_ms} average ms')