# coding: utf-8

"""
    Martlet Organization API

    Create/maintain organizations, access keys, addresses and permissions.   # noqa: E501

    OpenAPI spec version: 0.165.0
    Contact: apiteam@bmbix.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class UserProfilesResponse(object):
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
        'user_profiles': 'list[UserProfile]'
    }

    attribute_map = {
        'user_profiles': 'user_profiles'
    }

    def __init__(self, user_profiles=None):  # noqa: E501
        """UserProfilesResponse - a model defined in Swagger"""  # noqa: E501
        self._user_profiles = None
        self.discriminator = None
        if user_profiles is not None:
            self.user_profiles = user_profiles

    @property
    def user_profiles(self):
        """Gets the user_profiles of this UserProfilesResponse.  # noqa: E501


        :return: The user_profiles of this UserProfilesResponse.  # noqa: E501
        :rtype: list[UserProfile]
        """
        return self._user_profiles

    @user_profiles.setter
    def user_profiles(self, user_profiles):
        """Sets the user_profiles of this UserProfilesResponse.


        :param user_profiles: The user_profiles of this UserProfilesResponse.  # noqa: E501
        :type: list[UserProfile]
        """

        self._user_profiles = user_profiles

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
        if issubclass(UserProfilesResponse, dict):
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
        if not isinstance(other, UserProfilesResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
