import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt

from pathlib import Path
import sys

def main(input_file_name):
    df = pd.read_csv(data_folder / input_file_name, parse_dates=['date_x'])

    # remove unecessary columns
    df.drop(columns=['overview', 'crew', 'orig_title', 'country'], inplace=True)

    # keep only year
    df['publication_year'] = df['date_x'].dt.year
    df.drop(columns=['date_x'], inplace=True)

    # filter ensuring only Released movies are kept
    released_df = df[df['status'].str.contains('Released')]
    result_df = released_df.drop(columns=['status'])

    # filter for english movies
    english_movies_df = result_df[result_df['orig_lang'].str.contains('English')]
    english_movies = english_movies_df.drop(columns=['orig_lang'])

    # remove duplicate - but since who knows why they're duplicated, take the larger revenue
    result_sorted = english_movies.sort_values(by=['names', 'revenue'], ascending=False)
    result_sorted.drop_duplicates(subset=['names', 'publication_year'], keep='first', inplace=True)

    # remove any rows with empty data just incase
    result_sorted.dropna(inplace=True)

    # rename rows
    result_sorted = result_sorted.rename(columns={"names": "title", "genre" : "genres", "budget_x" : "budget", "publication_year" : "release_year"})

    # reorder rows
    result_sorted = result_sorted[['title' , 'release_year', 'genres', 'score', 'budget', 'revenue']]

    # print(result_sorted)
    result_sorted.to_csv(data_folder / 'imdb_movies_cleaned.csv', index=False)

    # flag weird discrepencies
    # that is names are the same and either same revenue or budget_x
    flag_revenue = result_sorted.copy()
    flag_budget = result_sorted.copy()

    # same name and revenue despite different other columns
    flag_revenue['duplicated_status'] = flag_revenue.duplicated(subset=['title', 'revenue'], keep=False)
    flag_revenue_filtered = flag_revenue[flag_revenue['duplicated_status'] == True]
    
    # remove the duplicated status column
    flag_revenue_filtered.drop(columns=['duplicated_status'])

    # same name and budget despite different other columns
    flag_budget['duplicated_status'] = flag_budget.duplicated(subset=['title', 'budget'], keep=False)
    flag_budget_filtered = flag_budget[flag_budget['duplicated_status'] == True]

    # remove the duplicated status column
    flag_budget_filtered.drop(columns=['duplicated_status'])

    flag_revenue_filtered.to_csv(data_folder / 'imdb_movies_duplicate_revenue_flagged.csv', index=False)
    flag_budget_filtered.to_csv(data_folder / 'imdb_movies_duplicate_budget_flagged.csv', index=False)

    ## PRINT FOR ADDITIONAL STATS
    # print(flag_revenue_filtered)
    # revenue_flag_output = flag_revenue_filtered.drop_duplicates(subset=['names'])
    # print(revenue_flag_output)
    
    # print(flag_budget_filtered)
    # budget_flag_output = flag_budget_filtered.drop_duplicates(subset=['names'])
    # print(budget_flag_output)


if __name__ == '__main__':

    data_folder = Path("data/")
    input_file_name = sys.argv[1]
    # output_file_name = sys.argv[2]

    main(input_file_name)
