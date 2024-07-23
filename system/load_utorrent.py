import os
import requests
import re

UTORRENT_URL = 'http://%s:%s/gui/' % ('localhost', '8080')
UTORRENT_URL_TOKEN = '%stoken.html' % UTORRENT_URL
REGEX_UTORRENT_TOKEN = r'<div[^>]*id=[\"\']token[\"\'][^>]*>([^<]*)</div>'

auth = requests.auth.HTTPBasicAuth('bob', 'hi')

def get_utorrent_token():
    r = requests.get(UTORRENT_URL_TOKEN, auth=auth)
    r.raise_for_status()
    token = re.search(REGEX_UTORRENT_TOKEN, r.text).group(1)
    return token, r.cookies['GUID']

def add_torrent(file_path, token, guid):
    headers = {'content-type': 'multipart/form-data'}
    params = {'action': 'add-file', 'token': token}
    files = {'torrent_file': open(file_path, 'rb')}
    r = requests.post(url=UTORRENT_URL, auth=auth, cookies=dict(GUID=guid), params=params, files=files)
    r.raise_for_status()
    print(f"Torrent {file_path} added successfully.")

def main():
    token, guid = get_utorrent_token()
    torrent_dir = r'C:\tor'
    for file_name in os.listdir(torrent_dir):
        if file_name.endswith('.torrent'):
            file_path = os.path.join(torrent_dir, file_name)
            add_torrent(file_path, token, guid)

if __name__ == '__main__':
    main()