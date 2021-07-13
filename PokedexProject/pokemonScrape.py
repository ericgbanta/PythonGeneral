# %% Import
import requests
from selenium import webdriver
import pandas as pd


# %% See website
url = 'http://pokemondb.net/pokedex/all'
driver = webdriver.Chrome(
    executable_path=r'C:\Users\eric.banta\Downloads\chromedriver_win32\chromedriver.exe')
driver.get(url)


# %% Scrape Tables
url = 'http://pokemondb.net/pokedex/all'
page = requests.get(url)

table = pd.read_html(page.text, header=0)

# %% Create DataFrame from List
df = pd.DataFrame(table[0])
df

# %% Clean Name and Type columns
# Write functions for cleaning


def cleanName(word):
    names = [x for x in word]
    for ltr in range(1, len(names)):
        if names[ltr].isupper():
            names[ltr] = ' ' + names[ltr]
    finalNames = ''.join(names).split(' ')
    length = len(finalNames)
    if length > 1:
        finalNames.insert(1, '(')
        finalNames.append(')')
    return ' '.join(finalNames)


def cleanType(word):
    types = [x for x in word]
    for ltr in range(1, len(types)):
        if types[ltr].isupper():
            types[ltr] = ' ' + types[ltr]
    finalTypes = ''.join(types).split(' ')
    return finalTypes


# Apply functions to DataFrame
df['Name'] = df['Name'].apply(cleanName)
df['Type'] = df['Type'].apply(cleanType)
df


# %% Store Data to JSON file
df.to_json(r'PokemonData.json')

# %% Peek at json file
pokemon = pd.read_json(r'PokemonData.json')
pokemon = pokemon.set_index(['#'])
pokemon.head()

# %% Save as CSV
pokemon.to_csv('PokemonData.csv')
