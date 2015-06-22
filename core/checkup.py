"""
This is the config file for the APIDoctor
module.

@package: APIDoctor
@version: 0.1
@module: checkup: This module runs the main checkup script
@author: Amyth Singh <mail@amythsingh.com>
"""


## Imports
import json

from config import settings
from utils import errors


class Checkup(object):
    """
    This is the main check-up class that runs requests over
    the set of API urls to log the timings and performance.
    """

    def __init__(self):
        """
        Sets required attributes to be used by the checkup script
        on class intialization.
        """

        self.server_url = settings.SERVER_URL
        self.info_file = settings.API_INFO_FILE
        self.avg_req_no = settings.AVERAGE_REQUESTS
        self.rtvars = settings.RTVARS
        self.request_queue = self.response_queue = []

        ## call the setup method
        self._setup()

    def _setup(self):
        """
        Sets up the environment for the checkup
        """

        ## First of, we set the runtime variables as the
        ## attributes of this class, so that they are
        ## accessible easily, when required. Currently
        ## we set their value as None, as they'll be updated
        ## once we have their value on runtime.
        for v in self.rtvars:
            setattr(self, v, None)

        ## Now we get the api resourse data that we need
        ## to use for checkup from the info json file and
        ## update the request queue.
        try:
            jfile = open(self.info_file, 'r')
            resources = json.loads(jfile.read())

            ## for each resource defined we add the object to the
            ## request queue. In case the index in the resource
            ## object is undefined, we simply append it to the
            ## queue else we add the object to the specified index
            for resource in resources:
                if not resource.get('index'):
                    self.request_queue.append(resource)
                else:
                    self.request_queue.insert(resource.get('index'), resource)
        except IOError as err:
            raise errors.ConfigurationError(str(err))
        except ValueError as err:
            raise errors.ConfigurationError(str(err))
