
# Thing Library

Library to interact and play round with thingiverse API and STL files. Contains a Flask front end, file downloader backend and stl viewer.   

Idea is to create the functionality to build a library of 3D objects based on specific search terms to be used in ML.


## Features

download_files:
- download all files for a single thing, searched for by ID.
- Search for multiple things by a search term or tag and download all files related to each thing.
- Verify things to select specific things to download

thingiverse_app: Frontend app built in flask
- Handles thingiverse web authentication to get access token
- (to do) front end for file download backend 

visualise_thing:
- load in stl files and view within Python 
- rotate files
- Resave files
- (to do) rescale and centre objects

## Usage/Examples

```python
# load thing
dogs = ThingDownloaderMulti()

# search for things tagged with dog, return 10 results
dogs.search_for_thing('tag', 'dog',per_page=10, sort = 'popular')

# verify through images and download verified things
dogs.verify_from_image()
dogs.download_verfied(file_path)

# download all items in the search
dogs.download_all(file_path)
```


## Reference

This package interacts with the thingiverse library. Before using the package, read the thingiverse terms of service: https://www.thingiverse.com/legal/api
