import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt

from pathlib import Path
import sys

# library for inflation
import cpi

def main(file1, file2, file3):
    df_1 = pd.read_csv(data_folder / file1)
    df_2 = pd.read_csv(data_folder / file2)

    complete_data = pd.concat([df_1, df_2], ignore_index=True)

    complete_data.drop_duplicates(subset=['title', 'release_year'], keep='first', inplace=True)

    complete_data_sorted = complete_data.sort_values(by=['title', 'release_year'], ascending=False)

    complete_data_sorted.drop_duplicates(subset=['title', 'budget'], keep='last', inplace=True)
    complete_data_sorted.drop_duplicates(subset=['title', 'revenue'], keep='last', inplace=True)

    # clean genre strings
    complete_data_sorted['genres'] = complete_data_sorted['genres'].str.strip('[]')
    complete_data_sorted['genres'] = complete_data_sorted['genres'].str.replace('\'', '', regex=False)

    # filter rows with improper data
    df_3 = pd.read_csv(data_folder / file3)
    df_3 = df_3[df_3['release_year'] != -1]
    df_3 = df_3[df_3['revenue'] != 0]

    merged_data = pd.merge(complete_data_sorted, df_3, 'left', left_on=['title', 'release_year'], right_on=['title', 'release_year'])
    merged_data['br_budget'] = ~(merged_data['budget_y'].isna())
    merged_data['br_revenue'] = ~(merged_data['revenue_y'].isna())
    merged_data.loc[merged_data['br_budget'] == False, 'budget'] = merged_data['budget_x']
    merged_data.loc[merged_data['br_revenue'] == False, 'revenue'] = merged_data['revenue_x']

    merged_data.loc[merged_data['budget_x'] >= merged_data['budget_y'], 'budget'] = merged_data['budget_x']
    merged_data.loc[merged_data['budget_x'] < merged_data['budget_y'], 'budget'] = merged_data['budget_y']
    merged_data.loc[merged_data['revenue_x'] >= merged_data['revenue_y'], 'revenue'] = merged_data['revenue_x']
    merged_data.loc[merged_data['revenue_x'] < merged_data['revenue_y'], 'revenue'] = merged_data['revenue_x']

    merged_data.drop(columns=['budget_x', 'revenue_x', 'budget_y', 'revenue_y', 'br_budget', 'br_revenue'], inplace=True)

    merged_data = merged_data[(merged_data['budget']) > 0];
    merged_data = merged_data[(merged_data['revenue']) >= 30];

    merged_data_sorted = merged_data.sort_values(by=['title', 'release_year'], ascending=False)

    merged_data_sorted.to_csv(output_folder / '0_movies_cleaned_final_concat.csv', index=False)

    # 2_b adjust for inflation

    movies = pd.read_csv(output_folder / "0_movies_cleaned_final_concat.csv")

    # drop rows where there is no pub year, box office value, and budget value just incase
    movies = movies.dropna(subset=['release_year', 'revenue', 'budget'])
    # movies.drop(columns=['runtime'], inplace=True)

    # get rid of movies that have revenue/budget values too low to be correct
    # get rid of movies from this year since it seems CPI does not have data for 2023 (not complete year?)
    movies_no_2023 = movies[(movies.release_year != 2023) & (movies.revenue >= 100000) & (movies.budget >= 100000)]

    # rename rows
    movies_no_2023 = movies_no_2023.rename(columns={"release_year": "year"})

    # convert years from float to int
    movies_no_2023['release_year'] = movies_no_2023['year'].astype(np.int64)
    movies_no_2023 = movies_no_2023.drop(columns=['year'])

    # update to get current inflation data
    # https://towardsdatascience.com/the-easiest-way-to-adjust-your-data-for-inflation-in-python-365490c03969
    cpi.update()

    # most recent 'complete' year is default so the 2022 isn't necessary, but just for clarity
    movies_no_2023['budget_adjusted'] = movies_no_2023.apply(lambda x: cpi.inflate(x['budget'], x['release_year'], to=2022), axis=1)
    movies_no_2023['revenue_adjusted'] = movies_no_2023.apply(lambda x: cpi.inflate(x['revenue'], x['release_year'], to=2022), axis=1)
    
    # print(movies_no_2023)

    movies_no_2023.to_csv(output_folder / "1_movies_adjusted_inflation.csv", index=False)

    # 2_c
    # generate genre csv

    next_set_movies = pd.read_csv(output_folder / "1_movies_adjusted_inflation.csv")
    next_set_movies['genres'] = next_set_movies['genres'].str.replace("action thriller", "Action, Thriller, ")
    next_set_movies['genres'] = next_set_movies['genres'].str.split(',')

    genres_exploded = next_set_movies.explode('genres', ignore_index=True)

    genres_exploded['genres'] = genres_exploded['genres'].str.strip()
    genres_exploded['genres'] = genres_exploded['genres'].str.replace(" film", "")
    genres_exploded['genres'] = genres_exploded['genres'].str.replace("books", "literature")
    genres_exploded['genres'] = genres_exploded['genres'].str.replace("a novel", "literature")
    genres_exploded['genres'] = genres_exploded['genres'].str.replace("speculative/", "")
    genres_exploded['genres'] = genres_exploded['genres'].str.capitalize()
    genres_exploded.dropna(inplace=True)

    genres_exploded.drop(genres_exploded[genres_exploded['genres'] == "Tv movie"].index, inplace = True)

    # print(genres_exploded)
    
    count = genres_exploded.groupby(['genres']).count()

    genres_exploded_sorted = genres_exploded.sort_values(by=['genres'])

    genres_exploded_sorted.to_csv(output_folder / "2_sorted_on_genres.csv", index=False)

    count.drop(columns=['score', 'budget', 'revenue', 'release_year', 'budget_adjusted', 'revenue_adjusted'], inplace = True)
    count = count.rename(columns={"title" : "count"})
    # print(count)
    count.to_csv(plot_folder / "genre_count.csv")


if __name__ == '__main__':

    data_folder = Path("data/")
    output_folder = Path("output/")
    plot_folder = Path("plot/")

    input_file_1 = sys.argv[1]
    input_file_2 = sys.argv[2]
    input_file_3 = sys.argv[3]


    main(input_file_1, input_file_2, input_file_3)
