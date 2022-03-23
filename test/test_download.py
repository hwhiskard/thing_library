import sys
import pytest

sys.path.append('..')


from src.download_files import ThingDownloader 

def test_api_connection():

    test_thing = ThingDownloader()
    
    user_details = test_thing.get_user_details()

    assert 'id' in user_details, "API connection failed"

test_api_connection()
