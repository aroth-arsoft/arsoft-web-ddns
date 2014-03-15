#!/usr/bin/python
# -*- coding: utf-8 -*-
# kate: space-indent on; indent-width 4; mixedindent off; indent-mode python;

import os
import os.path
import argparse
import sys
import logging
import time

import urllib2
import json

# version of this script
__version__  = '1.0'

def update_dns_record(service_url, hostname, address, password, recordtype='A'):
    params = {}
    params['host'] = hostname
    params['addr'] = address
    params['pw'] = password
    params['type'] = recordtype
    query = ''
    for (param_name, param_value) in params.iteritems():
        print((param_name, param_value))
        if len(query) > 0:
            query = query + '&'
        query = query + param_name + '=' + (param_value if param_value is not None else '')
    full_url = service_url + '/update?' + query
    
    print(full_url)
    
    try:
        response = urllib2.urlopen(full_url)
        if response:
            response_data = json.loads(response.read())
            if response.getcode() == 200:
                ret = True
            else:
                print(response_data)
                if 'error' in response_data:
                    print(response_data['error'])
                ret = False
        else:
            ret = False
    except urllib2.HTTPError as e:
        print(e)
        ret = False
    return ret

class ddnsApp(object):
    
    DEFAULT_SERVICE_URL = 'http://localhost:8000'
    
    def __init__(self):
        self.verbose = False
        self._config = None

    def version(self):
        print('Version: ' + str(__version__))
        return 0

    def main(self):
        #=============================================================================================
        # process command line
        #=============================================================================================
        parser = argparse.ArgumentParser(description='update a DNS record')
        parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='enable verbose output.')
        parser.add_argument('--version', dest='version', action='store_true', help='enable the version and exits.')
        parser.add_argument('--url', dest='service_url', default=self.DEFAULT_SERVICE_URL, type=str, help='URL of the DDNS web service.')
        parser.add_argument('--rrtype', dest='rrtype', default='A', type=str, help='type of the record to update.')
        parser.add_argument('--password', dest='password', type=str, help='password to access the DDNS web service.')
        parser.add_argument('hostname', type=str, help='name of the DNS record name')
        parser.add_argument('address', type=str, help='IP address for the DNS record')

        args = parser.parse_args()

        if args.version:
            return self.version()

        self.verbose = args.verbose
        
        if update_dns_record(args.service_url, args.hostname, args.address, args.password, args.rrtype):
            ret = 0
        else:
            print('update failed.')
            ret = 1
        
        return ret

if __name__ == "__main__":
    app =  ddnsApp()
    sys.exit(app.main())
