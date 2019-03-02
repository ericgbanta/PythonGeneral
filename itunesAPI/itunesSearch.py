# %% Import
import requests
import json
response = requests.get('https://itunes.apple.com/search?term=guns+and+roses&limit=1')

# view http status code of the response
response.status_code


# %% Search for artist or band and limit to 1 song
search = input('Search an artist: ')
search = search.replace(' ', '+')
a = ('https://itunes.apple.com/search?term=' + search + '&limit=1')
b = requests.get(a).json()
print(json.dumps(b, indent=2))


# %% Search by artist ID and return artist info:
search = int(input('Search by artist id: '))
search = str(search)
a = ('https://itunes.apple.com/lookup?id=' + search)
b = requests.get(a).json()
print(json.dumps(b, indent=2))


# %% Query all albumbs by artist ID:
search = int(input('Search by artist id: '))
search = str(search)
a = ('https://itunes.apple.com/lookup?id=' + search + '&entity=album')
b = requests.get(a).json()
print(json.dumps(b, indent=2))


# %% Return just artist name and genre
search = int(input('Search by artist id: '))
search = str(search)
a = ('https://itunes.apple.com/lookup?id=' + search)
b = requests.get(a).json()
print('Artist: {artist_name}, Genre: {genre_name}'.format(artist_name=b['results'][0]['artistName'],
                                                          genre_name=b['results'][0]['primaryGenreName']))
