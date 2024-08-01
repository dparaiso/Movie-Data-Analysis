import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import re

from pathlib import Path
import sys

currency = re.compile(r'(\d+) USD$')

percent = re.compile(r'(\d+)%')
fraction = re.compile(r'(\d+(\.\d+)?)/10')

def keep_USD(budget):
    if pd.isna(budget):
        return None
    else:
        response = currency.search(budget)
        if response:
            return int(response.group(1))
        else:
            return None

def turn_into_int(score):
    if pd.isna(score):
        return None
    else:
        response = percent.search(score)
        if response:
            return int(response.group(1))
        else:
            response = fraction.search(score)
            if response:
                return int(float(response.group(1))*10) 
            else:
                return None

def main(input_file_name):
    df = pd.read_csv(data_folder / input_file_name, parse_dates=['publicationdate'])

    # remove the wiki data link item
    df.drop(columns=['item'], inplace=True)

    # go through budget and keep only the ones with USD values
    df['cost']= df['budget'].apply(keep_USD)
    df.drop(columns=['budget'], inplace=True)

    # keep only year
    df['publication_year'] = df['publicationdate'].dt.year
    df.drop(columns=['publicationdate'], inplace=True)

    # use box office USA
    usa_box = df.drop(columns=['boxofficeusa'])

    # sort
    usa_result_sorted = usa_box.sort_values(by=['title', 'boxofficeww'], ascending=False)

    # remove duplicate genre
    genre_cleaned = usa_result_sorted.drop_duplicates(subset=['title', 'genreLabel'], keep='first')

    # merge all the genreLabel
    genre = genre_cleaned.groupby('title')['genreLabel'].agg(', '.join)

    # reset index
    genre = genre.reset_index()

    genre.rename(columns={'genreLabel':'genre_list', 'title':'movie_title'}, inplace=True)
    
    # combine movies with their total genre list
    usa_joined = usa_result_sorted.set_index('title').join(genre.set_index('movie_title'), how='inner')

    # drop original genre column
    usa_joined.drop(columns=['genreLabel'], inplace=True)

    # reset index
    usa_joined = usa_joined.reset_index(names='title')

    # there are a lot of duplicates with genres each generating a disctinct entry
    usa_result_filtered = usa_joined.drop_duplicates(subset=['title', 'publication_year'], keep='first')

    usa_result_filtered['score'] = usa_result_filtered['reviewscore'].apply(turn_into_int)
    usa_result_filtered.drop(columns=['reviewscore'], inplace=True)

    # final drops if desired
    usa_result_filtered.dropna(inplace=True)
    
    # rename rows
    usa_result_filtered = usa_result_filtered.rename(columns={"boxofficeww": "revenue", "genre_list" : "genres", "cost" : "budget", "publication_year" : "release_year"})

    # reorder rows
    usa_result_filtered = usa_result_filtered[['title' , 'release_year', 'genres', 'score', 'budget', 'revenue']]

    print(usa_result_filtered)
    # usa_result_filtered.to_csv(data_folder / 'wikiDataCleaned.csv')
    usa_result_filtered.to_csv(data_folder / 'wikiDataCleaned_1915.csv', index=False)

   

if __name__ == '__main__':

    data_folder = Path("data/")
    input_file_name = sys.argv[1]
    # output_file_name = sys.argv[2]

    main(input_file_name)
