#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from thumbor.handlers import ContextHandler
from thumbor.utils import logger
import tornado


class WhitelistDimensionsHandler(ContextHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        whitelist_dimensions = yield self.get_whitelist_dimensions_contents()

        self.write(whitelist_dimensions)
        self.set_header("Content-Type", "text/plain")
        self.set_status(200)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def put(self):
        whitelist_dimensions = yield self.get_whitelist_dimensions_contents()
        whitelist_dimensions += self.request.query + "\n"
        logger.debug("Adding to whitelist dimensions: %s", self.request.query)
        self.context.modules.storage.put("whitelist_dimensions.txt", whitelist_dimensions.encode())
        self.set_status(200)
