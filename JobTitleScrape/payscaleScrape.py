# %% Import
import requests
from selenium import webdriver
import pandas as pd
import numpy as np
import datetime
from string import ascii_uppercase
from lxml import html
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# %% BLOCK 1 - See website %% #
url = 'https://www.payscale.com/index/CA/Job/'
driver = webdriver.Chrome(
    executable_path=r'C:\Users\ericg\Downloads\chromedriver_win32\chromedriver.exe')
driver.get(url)


# %% BLOCK 2 - Scrape Tables for titles - OPTIONAL %% #
# Create 'Emoty DataFrame'
todays_date = datetime.datetime.now().date()
index = pd.date_range(
    todays_date - datetime.timedelta(10), periods=10, freq='D')
columns = ['A']

finalDF = []
finalDF = pd.DataFrame(index=index, columns=columns)

# Loop through all webpages and append job titles to dataframe
for letter in ascii_uppercase:
    df = []
    page = requests.get('https://www.payscale.com/index/CA/Job/' + letter)
    table = pd.read_html(page.text, header=0)
    # Create DataFrame from List
    df = pd.DataFrame(table[0])
    finalDF = finalDF.append(df)

# clean DataFrame
finalDF = finalDF.dropna(how='all')
finalDF = finalDF.drop('A', 1)
finalDF = finalDF.reset_index()
finalDF = finalDF.drop('index', 1)
finalDF


# %% BLOCK 3 - For each title, pull the link associated with each %% #
url = 'https://www.payscale.com'
urls = []

for letter in ascii_uppercase:
    page = requests.get('https://www.payscale.com/index/CA/Job/' + letter)
    tree = html.fromstring(page.text)
    links = tree.xpath('//tr/td/a/@href')
    urls = urls + links

urls = [url + link for link in urls]

print(urls)
print(len(urls))  # check if amount of links = amount of titles


# %% BLOCK 4 - Append urls to dataframe %% #
urlArray = np.asarray(urls)
data = finalDF.copy()
data['URLS'] = urlArray
data


# %% BLOCK 5 - Export to excel file
writer = pd.ExcelWriter('PayscaleExport.xlsx')
data.to_excel(writer, 'Sheet 1', index=None)
writer.save()
