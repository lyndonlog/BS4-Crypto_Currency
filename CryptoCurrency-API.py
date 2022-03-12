import csv
import time
from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd

def initiate():
    url_text = requests.get("https://www.coingecko.com/").text
    soup = BeautifulSoup(url_text, "lxml")
    container = soup.find_all("td", class_="py-0 coin-name cg-sticky-col cg-sticky-third-col px-0 tw-max-w-40 tw-w-40")
    price_container = soup.find_all('td', class_="td-price price text-right pl-0")
    abbreviation_container = soup.find_all("td", class_="py-0 coin-name cg-sticky-col cg-sticky-third-col px-0 tw-max-w-40 tw-w-40")

    name_list = []
    price_list = []
    abb_list = []

    """ I created a 3 list for name, abbreviation and price. Each name, price and abbreviation are appended
    into their designated list by using for loop. Then I used for loop again with using zip() grabbing the
     items in the lists so that I can iterate and print the names, abbreviations and prices in a parallel.
"""
    for item in container:
        name = item.find("a", class_="tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between").text
        name_list.append(name.strip()) #stripping html tag text
    for item2 in price_container:
        price = item2.find("span", class_="no-wrap").text
        price_list.append(price)
    for item3 in abbreviation_container:
        abbreviation = item3.find("span", class_="tw-hidden d-lg-inline font-normal text-3xs ml-2").text
        abb_list.append(abbreviation.strip()) #stripping html tag text

    number_order = 0 #For iterate the number order e.g. 1.) 2.)
    date_now = datetime.datetime.now()
    print(f"As of {date_now.strftime('%B %d, %Y %I:%M:%I %p %A')} ") #https://docs.python.org/3/library/datetime.html ==> for percent code
    print('NAME', 'ABBREVIATION', "PRICE", sep=" - ")   #separator
    print('--------------------------------------------------------------')
    for i, j, k in zip(name_list, abb_list, price_list):
        number_order += 1
        print(f"{number_order}.){i}", j, k, sep=" - ", end='\n--------------------------------------------------------------\n')
                                                        #per line ends with newspace then the string then newspace again


###################################################################
    """THIS CODE BELOW, FOR LOOP BELOW WILL STORE EACH DATA(EACH TXT FILE) TO "Each_Crypto" DIRECTORY"""
    for i, j, k in zip(name_list, abb_list, price_list):
        date_now = datetime.datetime.now()
        number_order = 0
        with open(f'Each_Crypto/{i}.txt', 'w') as f:
            number_order += 1
            f.write((f"As of {date_now.strftime('%B %d, %Y %I:%M:%I %p %A')}\n"))
            f.write(f"{i} - {j} - {k}")
###################################################################
    """"THIS CODE BELOW STORES THE SCRAPE DATA IN DIRECTORY AS CSV FILE """
    csv_file = open('CSV_Files/CSV_Crypto.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(name_list)
    csv_writer.writerow(abb_list)
    csv_writer.writerow(price_list)
###################################################################
    """THIS CODE BELOW CREATES A DATAFRAME USING PANDAS PYTHON LIB AND ALSO STORES THE DATA IN DIRECTORY AS CSV FILE"""
    data_frame1 = {'Name': name_list,
                   'Abbreviation': abb_list,
                   'Price': price_list
                   }

    df = pd.DataFrame(data_frame1)
    pd.set_option("max_colwidth", 20)
    pd.set_option('display.max_rows', 100)
    print(df)
    df.to_csv("CSV_Files/pandas-csv.csv", index=False) #index values will be disabled or won't be printed inside the csv file.
###########################################################

""" I want it to be endless program so I set a loop "while True" then every 1 minute it runs the initiate() function/method
    that scrapes data from coingecko.com and print the data on the Terminal e.g. Power Shell. """

if __name__ == "__main__":
    while True:
        initiate()
        print("waiting for 1 minute")
        time.sleep(60)