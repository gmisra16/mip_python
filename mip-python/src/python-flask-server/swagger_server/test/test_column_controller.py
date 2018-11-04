# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestColumnController(BaseTestCase):
    """ColumnController integration test stubs"""

    def test_add_column(self):
        """Test case for add_column

        Add a new column
        """
        response = self.client.open(
            '/v1/column',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_columns(self):
        """Test case for get_columns

        Finds Column by name
        """
        query_string = [('name', 'name_example')]
        response = self.client.open(
            '/v1/column',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
