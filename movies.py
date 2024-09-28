import csv
from collections import defaultdict
import time
import random

class Movie:
    def __init__(self, title : str, genre : str, year : int):     
        self.title = title
        self.genre = genre
        self.year = year
    def __repr__(self):
        return f'({self.title} : {self.year} : {self.genre})'

movie_list = [] # list of movie objects, assuming id=index
movie_dic = defaultdict(set)  # dictionary of sets, keyed on tuple(year, genre)
unique_years = set()
unique_genres = set()


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

                unique_years.add(year)

                genres = genre.split(',')
                for g in genres:
                    key = (year,g.casefold())
                    movie_dic[key].add(id)

                    unique_genres.add(g)

    #print(sorted(unique_years))
    #print(sorted(unique_genres))

load()


def get_uniques(genre: str = '', from_year: int = 0, to_year: int = 3000):
    ids = set()
    year_query = set(range(from_year, to_year+1)).intersection(unique_years)
    genre_query = (genre,) if genre != '' else unique_genres
    for y in year_query:
            for g in genre_query:
                key = (y, g.casefold())
                if key in movie_dic.keys():
                    ids.update(movie_dic[key])

    return [movie_list[x] for x in ids]


# retrieve movies in genre 'Animation', any date
res = get_uniques('animation')
print('### animation, any date ###')
print(res)

# retrieve movies in genre 'Action', 2006-2007
res = get_uniques('action', 2006, 2007)
print('### action, 2006-2007 ##')
print(res)

# retrieve movies for any genre, 2006
res = get_uniques('', 2006, 2006)
print('### any genre, 2006 ##')
print(res)


# test average retrieval time over 1000 random queries
def test_speed():
    trials = 1000*100
    tot_secs = 0
    for i in range(0, trials):
        genre = random.choice(list(unique_genres))
        year_from = random.choice(list(unique_years))
        year_to = random.choice([y for y in list(unique_years) if y >= year_from])
        tic =  time.perf_counter()
        movies = get_uniques(genre, year_from, year_to)
        toc = time.perf_counter()    
        tot_secs += (toc - tic)
    avg_secs = tot_secs / trials
    print(f'avg {avg_secs*1000} ms')

test_speed()