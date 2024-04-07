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
    ):
        self.logger = class_logger(__name__, self.__class__.__name__)
        self.url = url
        self._height = None

    async def height(self):
        response = requests.get(self.url + "/height")
        # 如果响应状态码为 200 OK，则处理响应内容
        if response.status_code == 200:
            print("Request was successful!")
            print("Response content:")
            print(response.text)
            self._height = int(response.text)
        else:
            print(f"Request failed with status code: {response.status_code}")
            # 可以根据具体的状态码做不同的处理
        return self._height

    def cached_height(self):
        '''Return the cached daemon height.

        If the daemon has not been queried yet this returns None.'''
        return self._height
