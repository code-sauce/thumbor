#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

import tempfile
from os.path import abspath, dirname, join

from preggy import expect
from tornado.testing import gen_test
from tests.base import TestCase
from thumbor.config import Config
from thumbor.context import Context
from thumbor.importer import Importer


class WhitelistDimensionsHandlerTestCase(TestCase):
    def get_context(self):
        file_storage_root_path = tempfile.TemporaryDirectory().name
        cfg = Config()
        cfg.USE_DIMENSIONS_WHITELIST = True
        cfg.LOADER = "thumbor.loaders.file_loader"
        cfg.FILE_LOADER_ROOT_PATH = abspath(
            join(dirname(__file__), "../fixtures/images/")
        )
        cfg.STORAGE = "thumbor.storages.file_storage"
        cfg.FILE_STORAGE_ROOT_PATH = file_storage_root_path
        importer = Importer(cfg)
        importer.import_modules()
        return Context(None, cfg, importer)

    @gen_test
    async def test_can_get_whitelist_dimensions(self):
        response = await self.async_fetch("/whitelist_dimensions")
        expect(response.code).to_equal(200)
        expect(response.body).to_equal("")

    @gen_test
    async def test_can_put_object_to_whitelist_dimensions(self):
        response = await self.async_fetch(
            "/whitelist_dimensions?20x30", method="PUT", body=""
        )
        expect(response.code).to_equal(200)
        expect(response.body).to_equal("")

    @gen_test
    async def test_can_read_updated_whitelist(self):
        await self.async_fetch("/whitelist_dimensions?100x200", method="PUT", body="")
        response = await self.async_fetch("/whitelist_dimensions")
        expect(response.code).to_equal(200)
        expect(b"100x200\n" in response.body).to_equal(True)

    @gen_test
    async def test_can_read_original_size(self):
        # note the image.jpg is of size 300x400

        # whitelist dimensions setting is
        response = await self.async_fetch("/unsafe/image.jpg")
        expect(response.code).to_equal(200)
        await self.async_fetch("/whitelist_dimensions?100x200", method="PUT", body="")

        # original size ok
        response = await self.async_fetch("/unsafe/image.jpg")
        expect(response.code).to_equal(200)

    @gen_test
    async def test_can_read_all_dimensions_if_no_whitelists(self):
        # whitelist dimensions setting is
        response = await self.async_fetch("/unsafe/image.jpg")
        expect(response.code).to_equal(200)

        response = await self.async_fetch("/unsafe/10x/image.jpg")
        expect(response.code).to_equal(200)

        response = await self.async_fetch("/unsafe/10x20/image.jpg")
        expect(response.code).to_equal(200)

    @gen_test
    async def test_can_read_only_whitelisted_dimensions(self):

        await self.async_fetch("/whitelist_dimensions?100x200", method="PUT", body="")

        response = await self.async_fetch("/unsafe/image.jpg")
        # original size ok
        expect(response.code).to_equal(200)

        response = await self.async_fetch("/unsafe/10x/image.jpg")
        expect(response.code).to_equal(400)

        response = await self.async_fetch("/unsafe/10x20/image.jpg")
        expect(response.code).to_equal(400)

        response = await self.async_fetch("/unsafe/100x200/image.jpg")
        expect(response.code).to_equal(200)
