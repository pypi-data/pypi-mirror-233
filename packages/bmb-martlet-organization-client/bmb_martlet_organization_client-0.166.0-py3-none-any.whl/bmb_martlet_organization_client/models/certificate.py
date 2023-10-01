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

class Certificate(object):
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
        'certificate_id': 'str',
        'data': 'str',
        'name': 'str',
        'media_type': 'str'
    }

    attribute_map = {
        'certificate_id': 'certificate_id',
        'data': 'data',
        'name': 'name',
        'media_type': 'media_type'
    }

    def __init__(self, certificate_id=None, data=None, name=None, media_type=None):  # noqa: E501
        """Certificate - a model defined in Swagger"""  # noqa: E501
        self._certificate_id = None
        self._data = None
        self._name = None
        self._media_type = None
        self.discriminator = None
        if certificate_id is not None:
            self.certificate_id = certificate_id
        if data is not None:
            self.data = data
        if name is not None:
            self.name = name
        if media_type is not None:
            self.media_type = media_type

    @property
    def certificate_id(self):
        """Gets the certificate_id of this Certificate.  # noqa: E501


        :return: The certificate_id of this Certificate.  # noqa: E501
        :rtype: str
        """
        return self._certificate_id

    @certificate_id.setter
    def certificate_id(self, certificate_id):
        """Sets the certificate_id of this Certificate.


        :param certificate_id: The certificate_id of this Certificate.  # noqa: E501
        :type: str
        """

        self._certificate_id = certificate_id

    @property
    def data(self):
        """Gets the data of this Certificate.  # noqa: E501


        :return: The data of this Certificate.  # noqa: E501
        :rtype: str
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this Certificate.


        :param data: The data of this Certificate.  # noqa: E501
        :type: str
        """

        self._data = data

    @property
    def name(self):
        """Gets the name of this Certificate.  # noqa: E501


        :return: The name of this Certificate.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Certificate.


        :param name: The name of this Certificate.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def media_type(self):
        """Gets the media_type of this Certificate.  # noqa: E501


        :return: The media_type of this Certificate.  # noqa: E501
        :rtype: str
        """
        return self._media_type

    @media_type.setter
    def media_type(self, media_type):
        """Sets the media_type of this Certificate.


        :param media_type: The media_type of this Certificate.  # noqa: E501
        :type: str
        """

        self._media_type = media_type

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
        if issubclass(Certificate, dict):
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
        if not isinstance(other, Certificate):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
