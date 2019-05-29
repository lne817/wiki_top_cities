# wiki_top_cities

Scrape the tables from Wikipedia pages into CSV files.

## Installation

Implemented in `Python3` with `Beautiful Soup`, `requests`, `lxml` parser.

```
# Install requirements from pip
pip install -r requirements.txt
```

## Use

1. n number of top cities by population can be initially scraped from the table on:
https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population
(example) `top_cities.csv`

2. New information using html tags on individual Wikipedia can be scraped, if exists, and added as a new column
(example) `top_cities_website.csv`

3. New information with href(link to an element) on individual Wikipedia pages can be scraped, if exists, and added as a new column
(example) `top_cities_website_time_zone.csv`, etc.


## Note
This script does not produce 100% clean data for every city query on Wikipedia, and should be improved, but we still can scrape data and add new information into the existing csv files.
