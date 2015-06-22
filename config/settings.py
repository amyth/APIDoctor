"""
This is the config file for the APIDoctor
module.

@package: APIDoctor
@version: 0.1
@module: config: This module contains all the configuration settings that are
                 used to run the APIDoctor module.
@author: Amyth Singh <mail@amythsingh.com>
"""

## The base server url where all the apis
## are served from
SERVER_URL = ''


## The json file that defines all the api
## paths request type and data to be sent
## for the requests
API_INFO_FILE = 'apis.json'


## Average number of requests to be made to
## an API
AVERAGE_REQUESTS = 5


## A list of runtime variables to be used in
## API requests
RTVARS = ['client_access_token', 'user_access_token']


## Here we try importing the variables defined
## in the personal settings file, so that they
## can be overriden. Putting this under a try
## except clause makes sure that, this even
## works for users who have not defined a personal
## settings file.
try:
    from config.personal import *
except:
    pass
