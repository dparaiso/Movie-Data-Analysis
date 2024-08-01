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

    # unadjusted average per year
    rev_avg = movies.groupby(by=['release_year'], as_index=False).mean()
    # print(rev_avg)

    plot_x = 12
    plot_y = 5

    # for unadjusted
    fig, ax = plt.subplots(figsize=(plot_x, plot_y))
    plt.scatter(rev_avg['release_year'], rev_avg['revenue'], marker='o', alpha=0.5)
    plt.title('Average Movie Box Office - Real World')
    plt.xlabel('Release Year')
    plt.ylabel('Revenue ($ USD)')
    plt.ylim(0,400000000)
    plt.ticklabel_format(style='plain')
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # plt.legend('Months')
    # plt.show()
    plt.savefig(output_plot / 'inflation_not_adjusted.png')

    # adjusted average per year
    rev_avg_adj = movies.groupby(by=['release_year'], as_index=False).mean()
    print(rev_avg_adj)

    # for adjusted
    fig, ax = plt.subplots(figsize=(plot_x, plot_y))
    plt.scatter(rev_avg_adj['release_year'], rev_avg_adj['revenue_adjusted'], marker='o', alpha=0.5)
    plt.title('Average Movie Box Office - Adjusted')
    plt.xlabel('Release Year')
    plt.ylabel('Revenue ($ USD)')
    plt.ticklabel_format(style='plain')
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # plt.show()
    plt.savefig(output_plot / 'inflation_adjusted.png')

    # for adjusted scaled
    fig, ax = plt.subplots(figsize=(plot_x, plot_y))
    plt.scatter(rev_avg_adj['release_year'], rev_avg_adj['revenue_adjusted'], marker='o', alpha=0.5)
    plt.title('Average Movie Box Office - Adjusted (Scaled)')
    plt.xlabel('Release Year')
    plt.ylabel('Revenue ($ USD)')
    plt.ylim(0,400000000)
    plt.ticklabel_format(style='plain')
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # plt.show()
    plt.savefig(output_plot / 'inflation_adjusted_scaled.png')


if __name__ == '__main__':
    working_directory = Path("output/")
    output_plot = Path("plot/")
    
    input = sys.argv[1]

    main(input)
