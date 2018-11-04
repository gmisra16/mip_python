# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestAirlinesController(BaseTestCase):
    """AirlinesController integration test stubs"""

    def test_get_airlines(self):
        """Test case for get_airlines

        Finds Airlines by name
        """
        query_string = [('name', 'name_example')]
        response = self.client.open(
            '/v1/airlines',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
