# Copyright (c) Sean
#
# All rights reserved.
#
# See the file "LICENCE" for information about the copyright
# and warranty status of this software.

'''Class for handling asynchronous connections to a ordinals node
daemon.'''

import asyncio
import itertools

import aiohttp
from electrumx.lib.util import (class_logger, json_deserialize)


class ServiceRefusedError(Exception):
    '''Internal - when the daemon doesn't provide a JSON response, only an HTTP error, for
    some reason.'''


class Ord:
    '''Handles connections to a daemon at the given URL.'''

    WARMING_UP = -28
    id_counter = itertools.count()

    def __init__(
            self,
            url,
            *,
            max_workqueue=10,
            init_retry=0.25,
            max_retry=4.0,
    ):
        self.logger = class_logger(__name__, self.__class__.__name__)
        self.url = url
        self.workqueue_semaphore = asyncio.Semaphore(value=max_workqueue)
        self.init_retry = init_retry
        self.max_retry = max_retry
        self._height = None
        self.session = None

        self._networkinfo_cache = (None, 0)
        self._networkinfo_lock = asyncio.Lock()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(connector=self.connector())
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.close()
        self.session = None

    def connector(self):
        return None


    async def _send_data(self, url):
        async with self.workqueue_semaphore:
            if self.session:
                async with self.session.get(url) as resp:
                    kind = resp.headers.get('Content-Type', None)
                    if kind == 'application/json':
                        return await resp.json(loads=json_deserialize)
                    text = await resp.text()
                    text = text.strip() or resp.reason
                    raise ServiceRefusedError(text)
            else:
                raise aiohttp.ClientConnectionError


    async def height(self):
        '''Query the daemon for its current height.'''
        self._height = await self._send_data(self.url+"/height")
        return self._height

    def cached_height(self):
        '''Return the cached daemon height.

        If the daemon has not been queried yet this returns None.'''
        return self._height
