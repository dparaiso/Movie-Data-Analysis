import numpy as np
import pandas as pd
import datetime

import seaborn
import matplotlib
import matplotlib.pyplot as plt

from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

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

    top_5 = top_genre_count.head(5)
    top_5 = top_5.rename(columns={"revenue_adjusted": "count"})
    ###

    genre_by_score = movies.copy()
    genre_by_score.drop(columns=['revenue_adjusted', 'budget', 'revenue', 'budget_adjusted'], inplace=True)

    average_score = genre_by_score.sort_values(by=['genres'])
    average_score.set_index('genres', inplace=True)
    # average_score.reset_index(inplace=True)

    # for 18
    result_score_18 = top_18.join(average_score, on=['genres'], how='inner')

    result_score_18.drop_duplicates(subset=['title', 'release_year'], inplace=True)
    result_score_18.drop(columns=['count', 'title'], inplace=True)

    # print(result_score_18)
    # return

    lin_regression = stats.linregress(result_score_18['release_year'], result_score_18['score'])

    result_score_18['predict_score'] = result_score_18['release_year'] * lin_regression.slope + lin_regression.intercept
    ###

    # for 5
    result_score_5 = top_5.join(average_score, on=['genres'], how='inner')
    result_score_5.drop(columns=['count'], inplace=True)

    ###

    # plot the scatter and line of best fit
    plt.figure(figsize=(12,6))
    plt.plot(result_score_18['release_year'], result_score_18['score'], 'g.', alpha=0.5, label='Score')
    plt.plot(result_score_18['release_year'], result_score_18['predict_score'], 'r-', linewidth=3, label='Best Fit Line')
    # plt.plot(result_score_5['release_year'], result_score_5['score'], 'r.', alpha=0.5)
    plt.title('Movie Scores')
    plt.xlabel('Release Year')
    plt.ylabel('Score (/100)')
    plt.legend()

    # plt.show()
    plt.savefig(output_plot / "score_scatter.png")

    # stats
    print("slope: ", lin_regression.slope, " intercept: ", lin_regression.intercept)
    print("p-value: ", lin_regression.pvalue)

    residuals = result_score_18['score'] - (lin_regression.slope * result_score_18['release_year'] + lin_regression.intercept)

    # plot the residule
    plt.figure(figsize=(12,6))
    plt.hist(residuals, bins=24)
    plt.title('Histogram of Residuals')
    plt.xlabel('Residual')
    plt.ylabel('Frequency')

    # plt.show()
    plt.savefig(output_plot / "score_residual_hist.png")

    # looks pretty normal, given the large number of entries, can be considered normal, but lets try and check anyways
    norm_test_result = stats.normaltest(residuals).pvalue

    print("normal test p-value: ", norm_test_result)

    # Check means of top 5 (Drama, Comedy, Thriller, Action, Adventure)

    result_score_5.reset_index(inplace=True)

    drama_movies = result_score_5[result_score_5['genres'] == 'Drama']
    comedy_movies = result_score_5[result_score_5['genres'] == 'Comedy']
    thriller_movies = result_score_5[result_score_5['genres'] == 'Thriller']
    action_movies = result_score_5[result_score_5['genres'] == 'Action']
    adventure_movies = result_score_5[result_score_5['genres'] == 'Adventure']

    
    plt.figure(figsize=(24,6))
    plt.suptitle('Histogram of Scores of Top 5 Genres')

    plt.subplot(1, 5, 1)
    plt.title('Drama Movies')
    plt.hist(drama_movies['score'], bins=20)
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    
    plt.subplot(1, 5, 2)
    plt.title('Comedy Movies')
    plt.hist(comedy_movies['score'], bins=20, color='red')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    
    plt.subplot(1, 5, 3)
    plt.title('Thriller Movies')
    plt.hist(thriller_movies['score'], bins=20, color='green')
    plt.xlabel('Score')
    plt.ylabel('Frequency')

    plt.subplot(1, 5, 4)
    plt.title('Action Movies')
    plt.hist(action_movies['score'], bins=20, color='orange')
    plt.xlabel('Score')
    plt.ylabel('Frequency')

    plt.subplot(1, 5, 5)
    plt.title('Adventure Movies')
    plt.hist(adventure_movies['score'], bins=20, color='purple')
    plt.xlabel('Score')
    plt.ylabel('Frequency')

    # plt.show()
    plt.savefig(output_plot / "top_5_genre_score_distribution.png")

    x1 = drama_movies['score']
    x2 = comedy_movies['score']
    x3 = thriller_movies['score']
    x4 = action_movies['score']
    x5 = adventure_movies['score']

    anova = stats.f_oneway(x1, x2, x3, x4, x5)
    print("ANOVA: ", anova.pvalue)

    # since value is small lets do the Post-Hoc
    x_data = pd.DataFrame({'Drama':x1, 'Comedy':x2, 'Thriller':x3, 'Action':x4, 'Adventure':x5})
    x_melt = pd.melt(x_data)
    x_melt = x_melt.dropna()

    post_hoc = pairwise_tukeyhsd(
        x_melt['value'], x_melt['variable'],
        alpha=0.05
    )

    print(post_hoc)

    fig = post_hoc.plot_simultaneous()
    # fig.suptitle("Comparison Between Genre Pairs (Tukey)")
    plt.title("Comparison Between Genre Pairs (Tukey)")
    plt.xlabel("Score (/100)")
    plt.ylabel("Genres")
    
    # plt.show()
    plt.savefig(output_plot / "tukey_spiffy_genres.png")

    # find the means
    score_mean = x_melt.groupby(by=['variable']).mean()
    score_mean.sort_values(by=['value'], ascending=True, inplace=True)
    print(score_mean)

if __name__ == '__main__':
    working_directory = Path("output/")
    output_plot = Path("plot/")

    input = sys.argv[1]

    main(input)