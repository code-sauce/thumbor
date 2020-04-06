#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from thumbor.handlers import ContextHandler
from thumbor.utils import logger


class WhitelistDimensionsHandler(ContextHandler):
    async def get(self):
        whitelist_dimensions = await self.get_whitelist_dimensions_contents()

        self.write(whitelist_dimensions)
        self.set_header("Content-Type", "text/plain")
        self.set_status(200)

    async def put(self):
        whitelist_dimensions = await self.get_whitelist_dimensions_contents()

        whitelist_dimensions += self.request.query + "\n"
        logger.debug("Adding to whitelist dimensions: %s", self.request.query)
        await self.context.modules.storage.put("whitelist_dimensions.txt", whitelist_dimensions.encode())
        self.set_status(200)
