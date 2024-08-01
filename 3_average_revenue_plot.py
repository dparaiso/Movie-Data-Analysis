import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import seaborn
import matplotlib.pyplot as plt
from pathlib import Path
import sys


def main(filename):
    data = pd.read_csv(output_dir / filename)

    # remove rows with empty genres
    data = data.dropna(subset=['genres'])

    # for report
    seaborn.set()    
    
    # keep only genres with sufficient number of samples
    genre_count = data.groupby(by='genres')['genres'].count()
    top_genres = genre_count[genre_count > 1250]
    data = data[data['genres'].isin(top_genres.index)]
    
    # have at least 3 samples of genre per year
    avg_revenue_per_genre_per_year = (data.groupby(['genres', 'release_year'])['revenue_adjusted'].agg([('count', 'size'), ('average_revenue', 'mean')]).reset_index())    
    avg_revenue_per_genre_per_year = avg_revenue_per_genre_per_year[avg_revenue_per_genre_per_year['count'] > 3]
    avg_revenue_per_genre_per_year = avg_revenue_per_genre_per_year.sort_values(['release_year', 'average_revenue'], ascending=False)

    grouped_avg_rev_per_genre = (avg_revenue_per_genre_per_year.groupby('release_year').agg(list)).reset_index()
    exploded_avg_rev_per_year = grouped_avg_rev_per_genre.explode(['genres', 'count', 'average_revenue']).reset_index(drop=True)
    exploded_avg_rev_per_year = exploded_avg_rev_per_year[['release_year', 'genres', 'average_revenue']]
    exploded_avg_rev_per_year = exploded_avg_rev_per_year.set_index('release_year')

    # colormap = plt.cm.jet
    # plt.gca().set_prop_cycle(plt.cycler('color', colormap(np.linspace(0, 1, 8))))
    
    # exploded_avg_rev_per_year.groupby('genres')['average_revenue'].plot(figsize=(15, 8), legend=True)
    
    # plt.title('Average Revenue Per Year from 1981')
    # plt.xlabel('Year')
    # plt.ylabel('Average Revenue')
    # plt.show()
    # plt.savefig("output/Average_Revenue_Per_Year_Plot.png")
    
    # Cleaner, more reliable data from 1981
    grouped_avg_rev_per_genre_1981 = grouped_avg_rev_per_genre[grouped_avg_rev_per_genre['release_year'] >= 1981]
    
    exploded_avg_rev_per_year_1981 = grouped_avg_rev_per_genre_1981.explode(['genres', 'count', 'average_revenue']).reset_index(drop=True)
    exploded_avg_rev_per_year_1981 = exploded_avg_rev_per_year_1981[['release_year', 'genres', 'average_revenue']]
    exploded_avg_rev_per_year_1981 = exploded_avg_rev_per_year_1981.set_index('release_year')


    fig0 = plt.figure()
    exploded_avg_rev_per_year_1981.groupby('genres')['average_revenue'].plot(figsize=(15, 8), legend=True)
    
    colormap = plt.cm.jet
    plt.gca().set_prop_cycle(plt.cycler('color', colormap(np.linspace(0, 1, 8))))
    
    plt.title('Average Revenue Per Year From 1981')
    plt.xlabel('Year')
    plt.ylabel('Average Revenue')
    # plt.show()
    fig0.savefig(plot_dir / "Average_Revenue_Per_Year_Plot.png")

    fig1 = plt.figure()
    exploded_avg_rev_per_year_1981.groupby('genres')['average_revenue'].hist(figsize=(15, 8), bins=20, legend=True)
    
    colormap = plt.cm.jet
    plt.gca().set_prop_cycle(plt.cycler('color', colormap(np.linspace(0, 1, 8))))
    
    plt.title('Average Revenue Per Year from 1981')
    plt.xlabel('Average Revenue')
    plt.ylabel('Number of Movies in Each Genre')
    # plt.show()
    fig1.savefig(plot_dir / "Average_Revenue_Per_Year_Histogram.png")

    # Transform right-skewed data with logarithm
    exploded_avg_rev_per_year_1981['log(average_revenue)'] = np.log(exploded_avg_rev_per_year_1981['average_revenue'].astype('float'))
    fig2 = plt.figure()
    exploded_avg_rev_per_year_1981.groupby('genres')['log(average_revenue)'].hist(figsize=(15, 8), bins=20, legend=True)

    colormap = plt.cm.jet
    plt.gca().set_prop_cycle(plt.cycler('color', colormap(np.linspace(0, 1, 8))))

    plt.title('Log of Average Revenue Per Year from 1981')
    plt.xlabel('Log of Average Revenue')
    plt.ylabel('Number of Movies in Each Genre')
    # plt.show()
    fig2.savefig(plot_dir / "Log_Average_Revenue_Per_Year_Histogram.png")
    
    # Narrow selection of genres to get better p-value for normality test and variance test
    selected_genres =['Drama', 'Comedy', 'Thriller', 'Action', 'Adventure', 'Crime']
    exploded_avg_rev_per_year_1981 = exploded_avg_rev_per_year_1981[exploded_avg_rev_per_year_1981['genres'].isin(selected_genres)]

    colormap = plt.cm.jet
    plt.gca().set_prop_cycle(plt.cycler('color', colormap(np.linspace(0, 1, 6))))

    fig3 = plt.figure()
    exploded_avg_rev_per_year_1981.groupby('genres')['log(average_revenue)'].hist(figsize=(15, 8), bins=20, legend=True)
    
    plt.title('Log of Average Revenue Per Year from 1981')
    plt.xlabel('Log of Average Revenue')
    plt.ylabel('Number of Movies in Each Genre')
    # plt.show()
    fig3.savefig(plot_dir / "Selected_Average_Revenue_Per_Year_Histogram.png")
    
    Drama = list(exploded_avg_rev_per_year_1981[exploded_avg_rev_per_year_1981['genres'] == 'Drama']['log(average_revenue)'])
    Comedy = list(exploded_avg_rev_per_year_1981[exploded_avg_rev_per_year_1981['genres'] == 'Comedy']['log(average_revenue)'])
    Thriller = list(exploded_avg_rev_per_year_1981[exploded_avg_rev_per_year_1981['genres'] == 'Thriller']['log(average_revenue)'])
    Action = list(exploded_avg_rev_per_year_1981[exploded_avg_rev_per_year_1981['genres'] == 'Action']['log(average_revenue)'])
    Adventure = list(exploded_avg_rev_per_year_1981[exploded_avg_rev_per_year_1981['genres'] == 'Adventure']['log(average_revenue)'])
    Crime = list(exploded_avg_rev_per_year_1981[exploded_avg_rev_per_year_1981['genres'] == 'Crime']['log(average_revenue)'])

    print(f'Normality Test p-values: \n Drama: {stats.normaltest(Drama).pvalue} \n Comedy: {stats.normaltest(Comedy).pvalue} \n Thriller: {stats.normaltest(Thriller).pvalue} \n Action: {stats.normaltest(Action).pvalue} \n Adventure: {stats.normaltest(Adventure).pvalue} \n Crime: {stats.normaltest(Crime).pvalue} \nLevene Test p-value: \n {stats.levene(Drama, Comedy, Thriller, Action, Adventure, Crime).pvalue}')

    posthoc = pairwise_tukeyhsd(
        exploded_avg_rev_per_year_1981['log(average_revenue)'], exploded_avg_rev_per_year_1981['genres'], alpha=0.05)

    print(posthoc)
    
    fig4 = posthoc.plot_simultaneous(figsize=(15, 8))
    plt.title("Comparison Between Genre Pairs (Tukey)")
    plt.xlabel("Average Revenue Per Year")
    plt.ylabel("Genres")
    # fig.show()
    fig4.savefig(plot_dir / "Selected_Average_Revenue_Per_Year_TukeyHSD.png")


if __name__ == '__main__':
    output_dir = Path("output/")
    plot_dir = Path("plot/")
    
    filename = sys.argv[1]

    main(filename)