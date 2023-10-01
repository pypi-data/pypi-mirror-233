# coding: utf-8

"""
    Martlet Organization API

    Create/maintain organizations, access keys, addresses and permissions.   # noqa: E501

    OpenAPI spec version: 0.166.0
    Contact: apiteam@bmbix.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class OrganizationProxyResponse(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'organization_proxy': 'OrganizationProxy'
    }

    attribute_map = {
        'organization_proxy': 'organization_proxy'
    }

    def __init__(self, organization_proxy=None):  # noqa: E501
        """OrganizationProxyResponse - a model defined in Swagger"""  # noqa: E501
        self._organization_proxy = None
        self.discriminator = None
        if organization_proxy is not None:
            self.organization_proxy = organization_proxy

    @property
    def organization_proxy(self):
        """Gets the organization_proxy of this OrganizationProxyResponse.  # noqa: E501


        :return: The organization_proxy of this OrganizationProxyResponse.  # noqa: E501
        :rtype: OrganizationProxy
        """
        return self._organization_proxy

    @organization_proxy.setter
    def organization_proxy(self, organization_proxy):
        """Sets the organization_proxy of this OrganizationProxyResponse.


        :param organization_proxy: The organization_proxy of this OrganizationProxyResponse.  # noqa: E501
        :type: OrganizationProxy
        """

        self._organization_proxy = organization_proxy

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(OrganizationProxyResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OrganizationProxyResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
