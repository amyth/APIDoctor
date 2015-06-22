"""
This is the config file for the APIDoctor
module.

@package: APIDoctor
@version: 0.1
@module: checkup: This module runs the main checkup script
@author: Amyth Singh <mail@amythsingh.com>
"""

## Imports
import csv
import json
import requests
import time

from config import settings
from utils import errors


PASSED = 'completed successfully'
FAILED = 'failed'


class Checkup(object):
    """
    This is the main check-up class that runs requests over
    the set of API urls to log the timings and performance.
    """

    def __init__(self, settings=settings):
        """
        Sets required attributes to be used by the checkup script
        on class intialization.
        """

        self.server_url = settings.SERVER_URL
        self.info_file = settings.API_INFO_FILE
        self.avg_req_no = settings.AVERAGE_REQUESTS
        self.rtvars = settings.RTVARS
        self.request_queue = self.response_queue = []
        self.decimals = settings.TIME_DECIMALS
        self.delay = settings.DELAY
        self.headers = settings.HEADERS

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

    def _to_seconds(self, t):
        """
        Converts the given time objsct into seconds
        """

        frmt = "{0:.%sf}" % (self.decimals)
        return float(frmt.format(t))

    def add_get_variables(self, url, data):
        """
        Adds the get variables to the url if any.
        """

        if data:
            return '%s?%s' % (url, urllib.urlencode(data))

        return url

    def get_request_headers(self, resource):
        """
        Returns the updated request headers for the given resource
        """

        headers = self.headers
        resource_headers = resource.get('headers')
        if resource_headers:
            headers.update(resource_headers)

        return headers

    def process(self):
        """
        Processes all the requests in the queue and log results.
        """


        csvfile = open('results.csv', 'wb')
        writer = csv.writer(csvfile)
        write_headers = ['Request %s' % q for q in range(
            1, self.avg_req_no + 1)]
        write_headers.insert(0, 'API Resource name')
        write_headers.append('Average Time')
        writer.writerow(write_headers)
        writer.writerow([]) # Adds an empty row after headers

        for resource in self.request_queue:
        
            times = 0
            time_list = []

            while times < self.avg_req_no:

                url = '%s%s' % (self.server_url, resource.get('path'))

                ## append get variables to the url if any
                url = self.add_get_variables(url, resource.get('get_data'))

                ## get request headers
                request_headers = self.get_request_headers(resource)
                request_method = resource.get('request_type').lower().strip()
                if request_method in ['post', 'put']:
                    data = resource.get('data', None)
                    if data:
                        data = json.dumps(data)

                ## make the request and store the response in a variable
                start_time = time.time()
                mtd = getattr(requests, request_method)
                response = mtd(url, data=data, headers=request_headers)
                end_time = time.time()

                ## Add delay right here
                time.sleep(self.delay)
                time_taken = end_time - start_time
                taken = self.to_seconds(time_taken)

                if response.status_code == resource.get('expected_status_code'):
                    response_status = PASSED
                else:
                    response_status = FAILED

                print 'Request for "%s" %s with status code %s.'\
                        ' Response time was %s.' % (
                        resource.get('name'), response_status,
                        response.status_code, taken)

                times += 1
                time_list.append(time_taken)

            avg_time = self._to_seconds(sum(time_list) / len(time_list))
            print "\nAverage time taken = %s\n" % avg_time

            time_list.append(avg_time)
            time_list.insert(0, resource.get('name'))
            writer.writerow(time_list)

        ## Add signature to the CSV file and close it
        writer.writerow([])
        writer.writerow([])
        writer.writerow([])
        writer.writerow(['CSV generated by APIDoctor 0.1 (@author: Amyth Singh)'])
        csvfile.close()

    def to_seconds(self, t):
        """
        Converts the given time objsct into seconds
        """

        return "%s second(s)" % self._to_seconds(t)

