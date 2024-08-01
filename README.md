# README

Since the data was obtained from multiple different sources. There are 4 different scripts to clean each of the data sets. \
See [1. Cleaning Data](#1-cleaning-data-sets)

To obtain the necessary files that were used for analysis, run the command with the arguments found here. \
See [2. Merging Data](#2-merging-data-sets)

The specific analysis is done in their individual files. There are 5 such scripts. \
See [3. Analysis](#3-analysis)

## 1. Cleaning Data Sets

### Wikidata
Cleaning the wikidata file `\data\3_MovieQuery1915.csv`

Run `python 1_wikidata_clean.py 3_MovieQuery1915.csv` \
This generates `wikiDataCleaned_1915.csv` in the `\data` folder

### Kaggle IMDB 
Cleaning the IMDB set from Kaggle `\data\imdb_movies.csv`

Run `python 1_imdb_kaggle_clean.py imdb_movies.csv` \
This generates `imdb_movies_cleaned.csv` in the `\data` folder

### ML IMDB data
Cleaning the IMDB Machine Learning set from
- `data\train_imdb.csv`
- `data\x_test_imdb.csv`
- `data\y_test_imdb.csv`
- `data\ratings.tsv`

This generates `imdb_output.csv` in the `\data` folder

### The Numbers data
> This may take up to a minute

Gathering & cleaning Movie Budgets data from [The Numbers - Movie Budgets](https://www.the-numbers.com/movie/budgets/all) \
This Generates `budget_revenue_data.csv` in the `\data` folder \

## 2. Merging Data Sets

All the data sets were then merged.
Movie budgets and revenues were adjusted for inflation.
Each genre was seperated from a comma seperated string list into individual items.

To run this file, the `cpi` library is needed for handling inflation.
See the [section on Inflation](#inflation) for more information.

Run `python 2_concat_data.py imdb_output.csv movies_cleaned_data_concat.csv budget_revenue_data.csv` \
This saves in the `\output` folder each intermediate step
- `0_movies_cleaned_final_concat.csv`
- `1_movies_adjusted_inflation.csv`
- `2_sorted_on_genres.csv`

## 3. Analysis

### Initial Data Visualization

The initial visualizations:

Revenue 

Run `python 3_initial_inflation_plot.py 1_movies_adjusted_inflation.csv` \
This generates 3 plots in the `\plot` directory
- `inflation_not_adjusted.png`
- `inflation_adjusted.png` 
- `inflation_adjusted_scaled.png`

Genre 

Run `python  3_initial_genre_plot.py  2_sorted_on_genres.csv` \
This generates 3 plots and 1 csv file in the `\plot` directory
- `Genre_Proportion.png`
- `Genre_Revenue_Box.png` 
- `Genre_Rating_Box.png`
- `popular_genre.csv`

### Average Revenue Per Year

Run `python 3_average_revenue_plot.py 2_sorted_on_genres.csv` \
This generates 5 plots in the `\plot` directory
- `Average_Revenue_Per_Year_Plot.png`
- `Average_Revenue_Per_Year_Histogram.png`
- `Log_Average_Revenue_Per_Year_Histogram.png`
- `Selected_Average_Revenue_Per_Year_1981_Histogram.png`
- `Selected_Average_Revenue_Per_Year_1981_TukeyHSD.png`

The statistical values are all printed in the console

### Measuring Success

#### Using Score

To generate the results of the
- Linear regression and resulting p-values
- ANOVA and Tukey Post Hoc Anlysis
- Order of Scores
- Related plots

Run `python 3_audience_scoring.py 2_sorted_on_genres.csv` \
This generates in the `\plot` directory
- `score_residual_hist.png`
- `score_scatter.png`
- `top_5_genre_score_distribution.png`
- `tukey_spiffy_genres.png`

The statistical values are all printed in the console

#### Using Profits

Run `python 3_profit_plot.py 2_sorted_on_genres.csv` \
This generates 1 plot in the `\plot` directory 
- `ROI_box.png`
- `ROI_no_duplicates_box.png` 

## Inflation
The library used to adjust for inflation is `cpi` <https://pypi.org/project/cpi/>
- Tested by installing it on Anaconda using `pip install cpi` but the pip method should be pretty universal
- Note that the inclusion of the library will increase code runtime
    - Might be due to some background updating or setup

Reference: <https://towardsdatascience.com/the-easiest-way-to-adjust-your-data-for-inflation-in-python-365490c03969>

### Known Error
I have occasionally run into an error like this when running \
`sqlite3.OperationalError: no such table: cu.data.2.Summaries`

If an error occurs when running, uninstall it `pip uninstall cpi`, reinstall it, and try running it again

## Wikidata

Wikidata SPARQL Query ran is stored in: `wikidataSPQLall.txt`

Property and Structuring of the Wikidata list for Movies: <https://www.wikidata.org/wiki/Wikidata:WikiProject_Movies/Properties>

The file `\data\3_MovieQuery1915.csv` is the result of the query. 
