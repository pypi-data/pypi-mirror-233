# coding: utf-8

"""
    Corva Data API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

from corva_data_assets.models.corva_asset_program import CorvaAssetProgram  # noqa: E501

class TestCorvaAssetProgram(unittest.TestCase):
    """CorvaAssetProgram unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CorvaAssetProgram:
        """Test CorvaAssetProgram
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CorvaAssetProgram`
        """
        model = CorvaAssetProgram()  # noqa: E501
        if include_optional:
            return CorvaAssetProgram(
                id = 4718,
                name = 'Uncon - Permian'
            )
        else:
            return CorvaAssetProgram(
        )
        """

    def testCorvaAssetProgram(self):
        """Test CorvaAssetProgram"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
