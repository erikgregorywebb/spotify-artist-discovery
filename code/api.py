import spotipy
import spotipy.util as util
import pandas as pd
import time

username = 'USERNAME-HERE'
scope = 'user-library-read'
client_id = 'CLIENT-ID-HERE'
client_secret = 'CLIENT-SECRET-HERE'
redirect_uri = 'https://example.com/callback'

token = util.prompt_for_user_token(
        username = username,
        scope = scope,
        client_id = client_id,
        client_secret = client_secret,
        redirect_uri = redirect_uri)

spotify = spotipy.Spotify(auth=token)

# create "links" table
a = spotify.artist('3TVXtAsR1Inumwj472S9r4') # drake
ra = spotify.artist_related_artists('3TVXtAsR1Inumwj472S9r4')

target_id = []
target_name = []
source_id = []
source_name = []
for artist in ra['artists']:
    target_id.append(artist['id'])
    target_name.append(artist['name'])
    source_id.append(a['id'])
    source_name.append(a['name'])
    
for i in range(0, 19):
    a = spotify.artist(target_id[i])
    ra = spotify.artist_related_artists(target_id[i])
    time.sleep(.5)
    #print(target_id[i])
    for artist in ra['artists']:
        target_id.append(artist['id'])
        target_name.append(artist['name'])
        source_id.append(a['id'])
        source_name.append(a['name'])
        
links = pd.DataFrame(list(zip(source_id, source_name, target_id, target_name)), 
             columns =['source_id', 'source_name', 'target_id', 'target_name']) 
             
# create "points" table             
all_artist_ids = list(set(source_id + target_id))

name = []
followers = []
popularity = []
url = []
image = []
for id in all_artist_ids:
    time.sleep(.5)
    a = spotify.artist(id)
    name.append(a['name'])
    followers.append(a['followers']['total'])
    popularity.append(a['popularity'])
    url.append(a['external_urls']['spotify'])
    image.append(a['images'][0]['url'])
    
points = pd.DataFrame(list(zip(all_artist_ids, name, followers, popularity, url, image)), 
             columns =['id', 'name', 'followers', 'popularity', 'url', 'image']) 
             
# export             
links.to_excel("links-drake.xlsx", index = False)
points.to_excel("points-drake.xlsx", index = False)             
