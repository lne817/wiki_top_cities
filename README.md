# wiki_top_cities

Scrape the tables from a Wikipedia article into CSV files.

## Installation

Implemented in [Python 3][python] with [Beautiful Soup][beautiful-soup], [requests][requests], [`lxml`][lxml] parser.

```
# Install requirements from pip
pip install -r requirements.txt
```

## Use

1. n number of top cities by population can be initially scraped from the table on:
https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population

New information with href(link to an element) on individual wiki pages can be added as a new column

Just import the module and call the `scrape` function. Pass it the full URL of a Wikipedia article, and a simple string (no special characters or filetypes) for the output name. The output will all be written to the `output_name` folder, with files named `output_name.csv`, `output_name_1.csv`, etc.


## Note
This script does not produce 100% clean data for every city query on Wikipedia, and should be improved, but we still can scrape data and add new information into the existing csv files.
