
import sys
import os

sys.path.append(r'C:\Users\Jefferson\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-packages')
from google_images_download import google_images_download   #importing the library

response = google_images_download.googleimagesdownload()   #class instantiation
artist = "chainsmokers"
arguments = {"keywords":artist,
             "limit":1,
             "print_urls":True, 
             "output_directory": "Artist",
             "no_directory": True,
             
             
             }   #creating list of arguments
paths = response.download(arguments)   #passing the arguments to the function
os.rename(str(paths[0]['chainsmokers'][0]),f'Artist/{artist}.png')



