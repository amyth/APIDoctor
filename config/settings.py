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


## Number of decimals to be shown with number
## of seconds a request took to be completed
TIME_DECIMALS = 3


## Delay (in number of seconds) in between the
## requests. Default is 5
DELAY = 1


## Generic request headers to be sent with each
## request.
HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
}

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
