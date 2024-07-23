# This is executed from an MS-DOS command on the 'sandbox windows VM'
#pip3 install requests

import requests
import math
import sys

sys.stdout.reconfigure(encoding='utf-8')

WS_URL = "https://yts.mx/api/v2/list_movies.json"
parameters = {'quality': '2160p', 'limit': 50}
response = requests.get(WS_URL, parameters)
js = response.json()

movie_count = js['data']['movie_count']
movie_limit = js['data']['limit']
page_number = js['data']['page_number']

print(f"TotalMovies:{movie_count}\n")
for movie_index in range(0, movie_count, 50):
   page = math.floor(movie_index/50) + 1
   WS_URL = "https://yts.mx/api/v2/list_movies.json"
   parameters = {'quality': '1080p', 'limit': 50, 'page':page}
   response = requests.get(WS_URL, parameters)
   js = response.json()
   for x in range(movie_limit):
      movie_num = x + movie_index
      slug = js['data']['movies'][x]['slug']
      title_long = js['data']['movies'][x]['title_long']
      description = js['data']['movies'][x]['description_full']
      print(f"\nNum:{movie_num} MovieName:{title_long}\nDescription:{description}")
      for z in js['data']['movies'][x]['torrents']:
         url = z['url']
         quality = z['quality']
         source = z['type']
         size_bytes = z['size_bytes']
         date_upload = z['date_uploaded']
         print(f"Slug:{slug} Quality:{quality} Type:{source} Size:{size_bytes} Date:'{date_upload}' URL:{url}")

