import numpy as np
import pandas as pd
import datetime

import seaborn
import matplotlib
import matplotlib.pyplot as plt

from pathlib import Path
import sys

def main(input):
    
    movies = pd.read_csv(working_directory / input)

     # for report
    seaborn.set()

    ###
    genre_by_year_revenue = movies.copy()
    genre_by_year_revenue.drop(columns=['title', 'score', 'release_year', 'budget', 'revenue', 'budget_adjusted'], inplace=True)

    # get top 18 genres based on avg
    top_genre_count = genre_by_year_revenue.groupby(['genres']).count()
    top_genre_count.sort_values(by=['revenue_adjusted'], ascending=False, inplace=True)

    top_18 = top_genre_count.head(18)
    top_18 = top_18.rename(columns={"revenue_adjusted": "count"})
    ###

    # genre count per year ###
    genre_by_year_count = movies.groupby(by=['release_year', 'genres'], as_index=False).count()

    genre_by_year_count.drop(columns=['score', 'budget', 'revenue', 'budget_adjusted', 'revenue_adjusted'], inplace=True)
    
    # take only top 18 genres with sufficeint entries
    genre_by_year_count.reset_index(drop=True, inplace=True)
    genre_by_year_count.set_index('genres')
    most_popular_genre = genre_by_year_count.join(top_18, on=['genres'], how='inner')

    most_popular_genre.reset_index(drop=True, inplace=True)

    most_popular_genre.set_index('release_year', inplace=True)
    
    # Lifted From SO to colour lines based on map
    # http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html
    colormap = plt.cm.jet
    plt.gca().set_prop_cycle(plt.cycler('color', colormap(np.linspace(0, 1, 18))))

    most_popular_genre.groupby('genres')['title'].plot(figsize=(15, 8), legend=True)
    
    plt.title('Genre Frequency')
    plt.xlabel('Release Year')
    plt.ylabel('Number of Movies Made')
    # plt.show()
    
    # print(most_popular_genre)

    plt.savefig(output_plot / "Genre_Proportion.png")
    most_popular_genre.to_csv(output_plot / "popular_genre.csv")

    ###

    # based on revenue - box plot ###

    # set index to join on
    genre_by_year_revenue.set_index('genres', inplace=True)

    # perform the join and clean it
    result_revenue = top_18.join(genre_by_year_revenue, on=['genres'], how='inner')
    result_revenue.drop(columns=['count'], inplace=True)

    # print(result_revenue)

    # plot it
    result_revenue.boxplot(by=['genres'], figsize=(20, 8))
    plt.title('Genre Revenues')
    plt.suptitle('')
    plt.xlabel('Genre')
    plt.yscale('log')
    plt.ylabel('Revenue ($ USD)')
    # plt.ylim(-0.05e10, 2e9)

    # plt.show()
    plt.savefig(output_plot / "Genre_Revenue_Box.png")
    
    ###

    # see score

    genre_by_score = movies.copy()
    genre_by_score.drop(columns=['title', 'revenue_adjusted', 'release_year', 'budget', 'revenue', 'budget_adjusted'], inplace=True)

    average_score = genre_by_score.groupby(['genres']).mean()

    genre_by_score.set_index('genres', inplace=True)

    result_score = top_18.join(genre_by_score, on=['genres'], how='inner')

    result_score.drop(columns=['count'], inplace=True)

    # plot it
    result_score.boxplot(by=['genres'], figsize=(20, 8))
    plt.title('Genre Ratings')
    plt.suptitle('')
    plt.xlabel('Genre')
    plt.ylabel('Rating (/100)')

    # plt.show()
    plt.savefig(output_plot / "Genre_Rating_Box.png")

    #### obtain statistic regarding how many movies are in the top 18 categories
    movies.reset_index(drop=True, inplace=True)
    movies.set_index('genres')
    num_movies_left = movies.join(top_18, on=['genres'], how='inner')
    num_movies_left.drop_duplicates(subset=['title'], keep='first', inplace=True)

    print(num_movies_left)

if __name__ == '__main__':
    working_directory = Path("output/")
    output_plot = Path("plot/")
    
    input = sys.argv[1]

    main(input)
