import pandas as pd 
import numpy as np

genreDictionary = {}

def myParser(listDict): 
    if listDict != []: 
        return [item['name'] for item in listDict]
    else: 
        return []

def genreCounter(genreList):
    for genre in genreList: 
        if genre in genreDictionary: 
            genreDictionary[genre] +=1
        else: 
            genreDictionary.update({genre : 1})

    return

def main(): 
    trainingData = pd.read_csv('data/train_imdb.csv')
    testData = pd.read_csv('data/x_test_imdb.csv')
    testRev = pd.read_csv('data/y_test_imdb.csv')
    ratings = pd.read_csv('data/ratings.tsv', sep='\t')
    extraData = pd.read_csv('data/data_1.csv')

    # merge the X_test with y_test
    fullTestData = pd.merge(testData, testRev, on="id", how="left")
    
    df = trainingData[['title', 'budget', 'genres', 'original_language', 'imdb_id', 'release_date', 'status',  'revenue']].copy()
    df2 = fullTestData[['title', 'budget', 'genres', 'original_language',  'imdb_id','release_date', 'status','revenue']].copy()
    
    # add the rows of df2 to df
    df = pd.concat([df,df2], axis=0)
    
    # eliminate rows with no budget
    df['budget'] = pd.to_numeric(df['budget'], errors='ignore')
    df = df[df['budget'] > 0]

    # convert release date and 
    df['release_date'] = pd.to_datetime(df['release_date'], format='%m/%d/%y')
    df = df[df['status'] == 'Released']
    df['release_year'] = df['release_date'].dt.year.astype(int)
    df['release_year'] = df['release_year'].map(lambda x: x if x < 2019 else x-100)

    # only keep english movies
    df = df[df['original_language'] == 'en']

    # drop movies with no title 
    df = df.dropna(axis = 0, subset=['title'])

    # merge with imdb ratings to get score column on imbd_id and tconst
    df = pd.merge(df, ratings, left_on='imdb_id', right_on='tconst')
    df['averageRating'] = df['averageRating'].apply(float)
    df = df[df['averageRating'] > 0]
    df['averageRating'] = df['averageRating'] *10

    # convert string to list of dictionaries 
    df['genres'] = df['genres'].apply(lambda x: list(eval(x)) if isinstance(x, str) else [])
    df['genres'] = df['genres'].apply(lambda x: myParser(x))

    # count instances of each genre
    # newDf['genres'].apply(lambda x: genreCounter(x))

    # rename ratings column to be concatenated
    df.rename(columns={'averageRating': 'score'}, inplace=True)

    # reorganize columns 
    df = df.reindex(columns=['title', 'release_year', 'genres', 'score', 'budget', 'revenue'])
    
    # concatenate extraData to the end of df 
    newDf = pd.concat([df, extraData], axis=0)

    # change from types string to int 
    newDf['revenue'] = newDf['revenue'].apply(int)
    newDf['budget'] = newDf['budget'].apply(int)

    # remove duplicates
    newDf = newDf.sort_values(by=['release_year', 'budget', 'revenue'])
    newDf = newDf.drop_duplicates(subset=['title','release_year'], keep='last')
    newDf = newDf.sort_values(by='title')

    # write results to output.csv
    newDf.to_csv('data/imdb_output.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    main()
