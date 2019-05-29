from bs4 import BeautifulSoup
import requests
import argparse
import csv
import warnings
warnings.filterwarnings("ignore")

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chrome/70.0.3538.77 Safari/537.36'}

def scrape_top_cities(in_file, n=20):
    """
    n: number of cities to scrape
    """

    url = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features="lxml")
    table = soup.find("table", {"class": "wikitable sortable"})
    colnames = ["2018 Rank", "City", "State", "2018 Estimate", "2010 Census", "Change", "2016 Land Area (sq mi)",
                "2016 Land Area (km^2)", "2016 Population Density (/sq mi)", "2016 Population Density (/km^2)", "Location"]

    with open(in_file, "w", newline="", encoding="utf8") as csvfile:
        
        writer = csv.DictWriter(csvfile, fieldnames=colnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        
        for row in table.find_all("tr")[:n+1]:
            cells = row.find_all("td")

            if (len(cells) > 0):
                
                scraped_data = {}
                
                for i in range(len(cells)):
                    text = cells[i].find_all(text=True)
                    scraped_data[colnames[i]] = text[0].replace(u'\n', u'')

                    if colnames[i] == "State":
                        scraped_data["State"] = text[1].replace(u'\n', u'')
                    if colnames[i] == "Location":
                        scraped_data["Location"] = "".join(text[0:3])

                scraped_data["2016 Land Area (sq mi)"] = scraped_data["2016 Land Area (sq mi)"].replace(u'\xa0sq\xa0mi', u'')
                scraped_data["2016 Land Area (km^2)"] = scraped_data["2016 Land Area (km^2)"].replace(u'\xa0km', u'')
                scraped_data["2016 Population Density (/sq mi)"] = scraped_data["2016 Population Density (/sq mi)"].replace(u'/sq\xa0mi', u'')
                scraped_data["2016 Population Density (/km^2)"] = scraped_data["2016 Population Density (/km^2)"].replace(u'/km', u'')

                writer.writerow(scraped_data)


def parse(url, link):

    success = False
    
    for retry in range(10):
        response = requests.get(url, verify=False, headers=headers)
        if response.status_code == 200:
            success = True
            break
        else:
            print("Response received: %s. Retrying : %s"%(response.status_code, url))
            success = False
    
    if success == False:
        print("Failed to process the URL: ", url)

    soup = BeautifulSoup(response.text, 'lxml')

    result = None

    if soup.find(href=link) is not None:
        parent = soup.find(href=link).parent.parent
        result = parent.find("td").find(text=True)

    return result


def add_with_href(in_file, arg):
    link = {"zip_code": "/wiki/ZIP_Code", "area_code": "/wiki/Telephone_numbering_plan", "gdp": "/wiki/GDP", "gmp": "/wiki/Gross_metropolitan_product",
            "time_zone": "/wiki/Time_zone"}

    out_file = in_file.replace(".csv", "_%s.csv" %(arg))

    with open(in_file, "r") as input_csv, open(out_file, "w", newline="", encoding="utf8") as output_csv:

        reader = csv.DictReader(input_csv)
        colnames = reader.fieldnames + [arg]
        writer = csv.DictWriter(output_csv, colnames)
        writer.writeheader()

        for row in reader:
            city = row["City"] + ", " + row["State"]
            if row["City"] == "Washington, D.C.":
                city = "Washington, D.C."
            url = "https://en.wikipedia.org/wiki/%s" %(city)
            print ("Retrieving :", url)
            result = parse(url, link[arg])
            row[arg] = result
            writer.writerow(row)

    return out_file


def add_with_tag(in_file, arg):
    
    out_file = in_file.replace(".csv", "_%s.csv" %(arg))

    with open(in_file, "r") as input_csv, open(out_file, "w", newline="", encoding="utf8") as output_csv:

        reader = csv.DictReader(input_csv)
        colnames = reader.fieldnames + [arg]
        writer = csv.DictWriter(output_csv, colnames)
        writer.writeheader()

        for row in reader:
            city = row["City"] + ", " + row["State"]
            if row["City"] == "Washington, D.C.":
                city = "Washington, D.C."
            url = "https://en.wikipedia.org/wiki/%s" %(city)
            print ("Retrieving :", url)
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, features="lxml")
            result = soup.select_one("th:contains(Website) + td > [href]")

            if result is not None:
                result = result["href"]

            row[arg] = result
            writer.writerow(row)

    return out_file

if __name__ == "__main__":

    in_file = "top_cities.csv"
    
    scrape_top_cities(in_file)

    out_file = add_with_tag(in_file, "website")
    out_file_1 = add_with_href(out_file, "time_zone")
    out_file_2 = add_with_href(out_file_1, "zip_code")
    out_file_3 = add_with_href(out_file_2, "gdp")
    out_file_4 = add_with_href(out_file_3, "gmp")
    
