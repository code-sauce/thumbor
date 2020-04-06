#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from preggy import expect

import thumbor.handler_lists.whitelist_dimensions as handler_list
from thumbor.handlers.whitelist_dimensions import WhitelistDimensionsHandler
from thumbor.testing import TestCase


class WhitelistDimensionsHandlerListTestCase(TestCase):
    def test_can_get_handlers(self):
        ctx = self.get_context()
        ctx.config.USE_DIMENSIONS_WHITELIST = True

        handlers = handler_list.get_handlers(ctx)

        expect(handlers).not_to_be_null()
        expect(handlers).to_length(1)
        url, handler, initializer = handlers[0]
        expect(url).to_equal(r"/whitelist_dimensions/?")
        expect(handler).to_equal(WhitelistDimensionsHandler)
        expect(initializer).to_equal({"context": ctx})

    def test_can_disable_whitelist_dimensions(self):
        ctx = self.get_context()
        ctx.config.USE_DIMENSIONS_WHITELIST = False

        handlers = handler_list.get_handlers(ctx)

        expect(handlers).not_to_be_null()
        expect(handlers).to_be_empty()
