import requests as r
import os
from PIL import Image
import matplotlib.pyplot as plt

api_base = "https://api.thingiverse.com/"

def get_api_path(base, access_token, search_term = None, *args):

    if search_term:
        api_query = base + search_term
    else:
        api_query = base

    api_query += '?'

    if args:
        for arg in args:
            api_query += arg + '&'
    else:
        api_query += '&'

    api_query += 'access_token=' + access_token

    return api_query

class ThingDownloader:

    def __init__(self):

        self.access_token = os.environ['ACCESS_TOKEN']

    def get_user_details(self):

        full_url = get_api_path(api_base, self.access_token, 'users/me')
        self.user_details = r.get(full_url).json()

        return self.user_details

    def search_for_thing(self,search_term,per_page, sort):

        search_path = f'search/{search_term}'
        num_results_path = f'per_page={per_page}'
        sort_path = f'sort={sort}'
        full_url = get_api_path(api_base, self.access_token, search_path, num_results_path, sort_path)
        self.search_results = r.get(full_url).json()

        return self.search_results

    def verify_from_image(self):

        for thing in self.search_results['hits']:
            print(thing["name"])
            print(thing["preview_image"])
            response = r.get(thing["preview_image"], stream=True)
            img = Image.open(response.raw)
            plt.imshow(img)
            plt.show()
            def get_input():
                while True:
                    correct_map = {'Y':True, 'N': False}
                    is_correct = input('Is object suitable (Y or N)?')
                    try:
                        return correct_map[is_correct]
                    except:
                        print('Enter Y or N')
            thing['is_correct'] = get_input()

    def download_verified(self, download_location):

        for thing in self.search_results['hits']:
            if thing['is_correct'] == True:
                    file_path = get_api_path(thing['url'] + '/files', self.access_token)
                    file_dict = r.get(file_path).json()
                    
                    for files in file_dict: 
                        print(files)
                        file_url = get_api_path(files['download_url'], self.access_token)
                        file = r.get(file_url)
                        file_name = os.path.join(download_location, thing['name'])
                        with open(file_name, 'wb') as f:
                            f.write(file.content)
        print('files downloaded')

    def get_thing_by_id(self, api_base, thing_id):

        search_term = f'things/{thing_id}'
        full_url = get_api_path(api_base, self.access_token, search_term)

        self.thing_json = r.get(full_url).json()
        

    def get_files(self):
        
        file_path = get_api_path(self.thing_json['files_url'], self.access_token)
        self.files = r.get(file_path).json()
        return self.files

    def download_files(self, download_location, limit = None):

        if limit is None:
            for thing in self.files:
                file_path = get_api_path(thing['download_url'], self.access_token)
                file = r.get(file_path)
                file_name = os.path.join(download_location, thing['name'])
                with open(file_name, 'wb') as f:
                     f.write(file.content)
                
            print('Files downloaded')

if __name__ == '__main__':

    # terrier = ThingDownloader()

    # terrier.get_thing_by_id(api_base,2334419)
    
    # thing_files = terrier.get_files()

    # file = terrier.download_files(r'C:\Users\WHI93526\OneDrive - Mott MacDonald\Documents\thing_files')

    dogs = ThingDownloader()
    dogs.search_for_thing('dog',per_page=3, sort = 'popular')
    dogs.verify_from_image()
    dogs.download_verified(r'C:\Users\WHI93526\OneDrive - Mott MacDonald\Documents\thing_files')

