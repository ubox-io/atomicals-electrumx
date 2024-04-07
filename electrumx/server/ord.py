# Copyright (c) Sean
#
# All rights reserved.
#
# See the file "LICENCE" for information about the copyright
# and warranty status of this software.

'''Class for handling asynchronous connections to a ordinals node
daemon.'''

import requests

from electrumx.lib.util import (class_logger, json_deserialize)


class ServiceRefusedError(Exception):
    '''Internal - when the daemon doesn't provide a JSON response, only an HTTP error, for
    some reason.'''


class Ord:
    '''Handles connections to a daemon at the given URL.'''

    def __init__(
            self,
            url,
            enable,
    ):
        self.logger = class_logger(__name__, self.__class__.__name__)
        self.url = url
        self.enable= enable
        self._height = None

    async def height(self):
        url = self.url + "/blockheight"
        response = requests.get(url)
        if response.status_code == 200:
            self._height = int(response.text)
        else:
            print(f"Ord Request failed with status code: {response.status_code}")
        return self._height

    def cached_height(self):
        '''Return the cached daemon height.

        If the daemon has not been queried yet this returns None.'''
        return self._height
