import requests as r
import os
from PIL import Image
import matplotlib.pyplot as plt

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

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

def cleanse_path(path_string):
    cleansed_name = ""
    
    for char in path_string:
        if (char.isalnum()):
            cleansed_name += char

    return cleansed_name

def download_files_from_thing(self, thing, download_location):
    folder_name = cleanse_path(thing['name'])
    folder_path = os.path.join(download_location, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = get_api_path(thing['url'] + '/files', self.access_token)
    file_dict = r.get(file_path).json()

    for file in file_dict: 
        #print(file)
        file_url = get_api_path(file['download_url'], self.access_token)
        file_dl = r.get(file_url)
        file_name = os.path.join(folder_path, file['name'])
        with open(file_name, 'wb') as f:
            f.write(file_dl.content)

class ThingDownloaderSingle:
    """
    Download things for a single thing by ID
    """
    def __init__(self):

        self.access_token = os.environ['ACCESS_TOKEN']

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
            for file in self.files:
                file_path = get_api_path(file['download_url'], self.access_token)
                file_dl = r.get(file_path)
                
                folder_name = cleanse_path(self.thing_json['name'])
                folder_path = os.path.join(download_location, folder_name)
                
                if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                file_name = os.path.join(folder_path, file['name'])
                with open(file_name, 'wb') as f:
                     f.write(file_dl.content)
                
            print('Files downloaded')


class ThingDownloaderMulti:
    """
    Download files for multiple things at once 
    """
    def __init__(self):

        self.access_token = os.environ['ACCESS_TOKEN']

    def get_user_details(self):

        full_url = get_api_path(api_base, self.access_token, 'users/me')
        self.user_details = r.get(full_url).json()

        return self.user_details

    def search_for_thing(self, search_type, search_term,per_page, sort):
        
        assert search_type == 'tag' or search_type == 'term', ' Search type must be either tag or term'

        search_path = f'search/{search_term}'
        if search_term == 'tag':
            search_path += 'tag'
        
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

                download_files_from_thing(self, thing, download_location)

        print('files downloaded')

    def download_all(self, download_location):

            for thing in self.search_results['hits']:
                print('downloading :', thing['name'])
                download_files_from_thing(self, thing, download_location)




if __name__ == '__main__':

    # terrier = ThingDownloaderSingle()

    # terrier.get_thing_by_id(api_base,2334419)
    
    # thing_files = terrier.get_files()

    # file = terrier.download_files(r'C:\Users\WHI93526\OneDrive - Mott MacDonald\Documents\thing_files')

    dogs = ThingDownloaderMulti()
    dogs.search_for_thing('tag', 'dragon',per_page=3, sort = 'popular')
    #dogs.verify_from_image()
    dogs.download_all(r'C:\Users\WHI93526\OneDrive - Mott MacDonald\Documents\thing_files')

