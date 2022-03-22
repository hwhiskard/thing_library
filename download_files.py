import requests as r
import os
from dotenv import load_dotenv

load_dotenv()

access_token = os.environ['ACCESS_TOKEN']
api_base = "https://api.thingiverse.com/"

def get_api_path(base, access_token):

    full_api_path = base + '?access_token=' + access_token
    return full_api_path

class ThingDownloader:

    def search_for_thing(self,search_term):

        api_path = api_base + f'search/{search_term}/'

        full_url = get_api_path(api_path, access_token)
        self.search_results = r.get(full_url).json()

        return self.search_results


    def get_thing_by_id(self, api_base, thing_id, access_token):

        api_path = api_base + f'things/{thing_id}'

        full_url = get_api_path(api_path, access_token)

        self.thing_json = r.get(full_url).json()
        

    def get_files(self):
        file_path = get_api_path(self.thing_json['files_url'], access_token)
        self.files = r.get(file_path).json()
        return self.files

    def download_files(self, download_location, limit = None):

        if limit is None:
            for thing in self.files:
                file_path = get_api_path(thing['download_url'], access_token)
                file = r.get(file_path)
                file_name = os.path.join(download_location, thing['name'])
                with open(file_name, 'wb') as f:
                     f.write(file.content)
                
            print('Files downloaded')

if __name__ == '__main__':

    terrier = ThingDownloader()

    terrier.get_thing_by_id(api_base,2334419,access_token)
    
    thing_files = terrier.get_files()

    file = terrier.download_files(r'C:\Users\WHI93526\OneDrive - Mott MacDonald\Documents\thing_files')

    search = ThingDownloader()

    searchres = search.search_for_thing('dog')