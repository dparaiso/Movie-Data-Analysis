import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from pathlib import Path


def main():
    base_url = 'https://www.the-numbers.com/movie/budgets/all'
    urls = []
    page = 0

    # Create a list of urls of all pages
    while page != 65:
        urls.append(f'{base_url}/{page*100 + 1}')
        page += 1

    # Build a dictionary from the data
    dict = {}
    for url in urls:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        page_soup = soup(webpage, 'html.parser')
        container = page_soup.findAll("td")
        
        for i in range(int(len(container)/6)):
            i *= 6
            title = container[i+2].text
            release_year = container[i+1].text[-5:]
            if (release_year.isalpha()):
                release_year = '-1'
            else:
                release_year = int(release_year)

            budget = container[i+3].text.replace(",","")
            revenue = container[i+5].text.replace(",","")
            if (budget[1:2] == '0'):
                budget = 0
            
            if (revenue[1:2] == '0'):
                revenue = 0

            budget = int(budget[2:])
            revenue = int(revenue[2:])


            title_year = (title, release_year)
            dict[title_year] = {}
            dict[title_year]['budget'] = budget;
            dict[title_year]['revenue'] = revenue;

    # Export dictionary as a csv file
    df = pd.DataFrame.from_dict(dict, orient='index')
    df = df.reset_index(names=['title', 'release_year'])
    df.to_csv(output_dir / 'budget_revenue_data.csv', index=False)


if __name__ == '__main__':
    output_dir = Path("data/")    

    main()