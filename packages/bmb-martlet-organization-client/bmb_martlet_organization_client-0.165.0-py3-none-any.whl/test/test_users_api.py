# coding: utf-8

"""
    Martlet Organization API

    Create/maintain organizations, access keys, addresses and permissions.   # noqa: E501

    OpenAPI spec version: 0.165.0
    Contact: apiteam@bmbix.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import bmb_martlet_organization_client
from bmb_martlet_organization_client.api.users_api import UsersApi  # noqa: E501
from bmb_martlet_organization_client.rest import ApiException


class TestUsersApi(unittest.TestCase):
    """UsersApi unit test stubs"""

    def setUp(self):
        self.api = UsersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_count_messages(self):
        """Test case for count_messages

        get unread, unprocessed message counts for the user  # noqa: E501
        """
        pass

    def test_create_organization(self):
        """Test case for create_organization

        Create an organization  # noqa: E501
        """
        pass

    def test_create_payment_method(self):
        """Test case for create_payment_method

        Record a payment method for the user  # noqa: E501
        """
        pass

    def test_create_payment_method_from_stripe_intent(self):
        """Test case for create_payment_method_from_stripe_intent

        Generate a Bmbix payment method from a successful Stripe Intent  # noqa: E501
        """
        pass

    def test_create_payment_method_link(self):
        """Test case for create_payment_method_link

        Record the link between a payment method and an organization  # noqa: E501
        """
        pass

    def test_create_private_key(self):
        """Test case for create_private_key

        Rotate private key - create and store new key with life of 90 days.   # noqa: E501
        """
        pass

    def test_delete_payment_method(self):
        """Test case for delete_payment_method

        Delete a payment method  # noqa: E501
        """
        pass

    def test_delete_payment_method_link(self):
        """Test case for delete_payment_method_link

        Delete a payment method link  # noqa: E501
        """
        pass

    def test_get_payment_method(self):
        """Test case for get_payment_method

        Get the payment methods for the user.  # noqa: E501
        """
        pass

    def test_get_payment_method_link(self):
        """Test case for get_payment_method_link

        Get a payment method link.  # noqa: E501
        """
        pass

    def test_get_public_key(self):
        """Test case for get_public_key

        Get the public key for a resource  # noqa: E501
        """
        pass

    def test_get_settings(self):
        """Test case for get_settings

        Get the user's settings  # noqa: E501
        """
        pass

    def test_get_stripe_intent(self):
        """Test case for get_stripe_intent

        Connect a user via Stripe  # noqa: E501
        """
        pass

    def test_get_user_certificate(self):
        """Test case for get_user_certificate

        \"Get the certificate for a user.\"   # noqa: E501
        """
        pass

    def test_list_organizations(self):
        """Test case for list_organizations

        list organizations for the user  # noqa: E501
        """
        pass

    def test_list_payment_method_links(self):
        """Test case for list_payment_method_links

        Get the payment methods links for the user.  # noqa: E501
        """
        pass

    def test_list_payment_methods(self):
        """Test case for list_payment_methods

        Get the payment methods for the user.  # noqa: E501
        """
        pass

    def test_list_permissions(self):
        """Test case for list_permissions

        Get the permissions for the logged-in user.  # noqa: E501
        """
        pass

    def test_list_private_keys(self):
        """Test case for list_private_keys

        Get the private keys for a resource.  # noqa: E501
        """
        pass

    def test_set_user_certificate(self):
        """Test case for set_user_certificate

        Upload a new X.509 identity certificate   # noqa: E501
        """
        pass

    def test_update_language(self):
        """Test case for update_language

        Update the self-provided language  # noqa: E501
        """
        pass

    def test_update_name(self):
        """Test case for update_name

        Update the self-provided name  # noqa: E501
        """
        pass

    def test_update_private_key(self):
        """Test case for update_private_key

        Update a private key.  set_rescinded ============= {   \"op\": \"replace\",   \"path\": \"/rescinded\",   \"value\": true }   # noqa: E501
        """
        pass

    def test_update_timezone(self):
        """Test case for update_timezone

        Update the self-provided timezone  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
