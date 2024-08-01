import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import re 
import seaborn

genre_film = re.compile(r'(\S*) film')

def strip_genre(genre):
    m = genre_film.match(genre)
    if m: 
        return m.group(1)
    else: 
        return genre
    
def main(input): 
    all_movies = pd.read_csv('output/' + input)

    # cleaning data
    all_movies.dropna(subset=['genres'], axis=0, inplace=True)
    all_movies['genres'] = all_movies['genres'].str.strip()
    all_movies['genres'] = all_movies['genres'].apply(strip_genre)
    all_movies['genres'] = all_movies['genres'].str.lower()
    all_movies['ROI'] = (all_movies['revenue_adjusted']-all_movies['budget_adjusted'])/all_movies['budget_adjusted']*100

    # copy dataframe
    movie_copy = all_movies.copy()
    action = all_movies.copy()
    drama = all_movies.copy()
    comedy = all_movies.copy()
    adventure = all_movies.copy()
    thriller = all_movies.copy()

    # filter dataframe
    action = action[action['genres']=='action']
    drama = drama[drama['genres']=='drama']
    comedy = comedy[comedy['genres']=='drama']
    adventure = adventure[adventure['genres']=='drama']
    thriller = thriller[thriller['genres']=='drama']

    # count genres
    all_movies = all_movies.groupby(['genres']).aggregate({'genres': 'count', 'budget_adjusted': 'mean', 'revenue_adjusted':'mean'}).rename_axis('genre_index').reset_index()
    all_movies.columns = ['genres', 'count', 'budget_adjusted', 'revenue_adjusted']

    # get top 5 columns
    all_movies = all_movies.sort_values(by=['count'], ascending=False).head(5)
    plot = pd.merge(all_movies[['genres','count']], movie_copy, on='genres', how='outer')
    plot.dropna(subset=['count'], axis=0, inplace=True)
    plot1 = plot.copy()
    plot2 = plot.copy()
    plot1 = plot1[['genres', 'ROI']]
    plot2 = plot2[['genres', 'ROI', 'title']]


    # plot data 
    seaborn.set()
    plot1.boxplot(by=['genres'], figsize=(15,10))
    plt.xlabel('Genres')
    plt.ylabel('Return on Investment Percentage')
    plt.yscale('symlog')
    plt.title('Top 5 Genres Return on Investment')

    plt.savefig('plot/ROI_box.png')

    plot2.drop_duplicates(subset='title',keep=False, inplace=True)
    plot2.drop(columns='title')
    plot2.boxplot(by=['genres'], figsize=(15,10))
    plt.xlabel('Genres')
    plt.ylabel('Return on Investment Percentage')
    plt.yscale('symlog')
    plt.title('Top 5 Genres Return on Investment')
    plt.savefig('plot/ROI_no_duplicates_box.png')
    
    # anova test results
    anova = stats.f_oneway(action['ROI'], drama['ROI'], comedy['ROI'], adventure['ROI'], thriller['ROI'])
    print('anova p-value: ', anova.pvalue)


if __name__ == '__main__':
    input = sys.argv[1]
    main(input)
