import pandas as pd
from pathlib import Path
import sys

def main(data_filename, br_data_filename):
    data = pd.read_csv(data_directory / data_filename)
    br_data = pd.read_csv(data_directory / br_data_filename)

    br_data = br_data[br_data['release_year'] != -1]
    br_data = br_data[br_data['revenue'] != 0]

    merged_data = pd.merge(data, br_data, 'left', left_on=['title', 'release_year'], right_on=['title', 'release_year'])
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

    merged_data.sort_values('title', inplace=True)

    # merged_data = merged_data[['title', 'release_year', 'score', 'budget', 'revenue']]

    merged_data.to_csv(output_directory / '0_movies_data.csv', index=False)
    

if __name__ == '__main__':
    data_directory = Path("data/")
    output_directory = Path("output/")
    data_filename = sys.argv[1]
    br_data_filename = sys.argv[2]

    main(data_filename, br_data_filename)
