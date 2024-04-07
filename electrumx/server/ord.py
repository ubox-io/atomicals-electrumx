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

    async def _send_data(self, url):
        async with requests.get(url) as resp:
            kind = resp.headers.get('Content-Type', None)
            if kind == 'application/json':
                return await resp.json(loads=json_deserialize)
            text = await resp.text()
            text = text.strip() or resp.reason
            raise ServiceRefusedError(text)


    async def height(self):
        '''Query the daemon for its current height.'''
        self._height = await self._send_data(self.url + "/height")
        return self._height


    def cached_height(self):
        '''Return the cached daemon height.

        If the daemon has not been queried yet this returns None.'''
        return self._height
