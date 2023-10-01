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

class PrivateKey(object):
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
        'private_key_id': 'str',
        'passphrase': 'str',
        'data': 'str',
        'bri': 'str',
        'fingerprint': 'str',
        'updated_at': 'str',
        'created_at': 'str',
        'expires_at': 'str',
        'rescinded': 'bool',
        'user_supplied': 'bool'
    }

    attribute_map = {
        'private_key_id': 'private_key_id',
        'passphrase': 'passphrase',
        'data': 'data',
        'bri': 'bri',
        'fingerprint': 'fingerprint',
        'updated_at': 'updated_at',
        'created_at': 'created_at',
        'expires_at': 'expires_at',
        'rescinded': 'rescinded',
        'user_supplied': 'user_supplied'
    }

    def __init__(self, private_key_id=None, passphrase=None, data=None, bri=None, fingerprint=None, updated_at=None, created_at=None, expires_at=None, rescinded=None, user_supplied=None):  # noqa: E501
        """PrivateKey - a model defined in Swagger"""  # noqa: E501
        self._private_key_id = None
        self._passphrase = None
        self._data = None
        self._bri = None
        self._fingerprint = None
        self._updated_at = None
        self._created_at = None
        self._expires_at = None
        self._rescinded = None
        self._user_supplied = None
        self.discriminator = None
        if private_key_id is not None:
            self.private_key_id = private_key_id
        if passphrase is not None:
            self.passphrase = passphrase
        if data is not None:
            self.data = data
        if bri is not None:
            self.bri = bri
        if fingerprint is not None:
            self.fingerprint = fingerprint
        if updated_at is not None:
            self.updated_at = updated_at
        if created_at is not None:
            self.created_at = created_at
        if expires_at is not None:
            self.expires_at = expires_at
        if rescinded is not None:
            self.rescinded = rescinded
        if user_supplied is not None:
            self.user_supplied = user_supplied

    @property
    def private_key_id(self):
        """Gets the private_key_id of this PrivateKey.  # noqa: E501


        :return: The private_key_id of this PrivateKey.  # noqa: E501
        :rtype: str
        """
        return self._private_key_id

    @private_key_id.setter
    def private_key_id(self, private_key_id):
        """Sets the private_key_id of this PrivateKey.


        :param private_key_id: The private_key_id of this PrivateKey.  # noqa: E501
        :type: str
        """

        self._private_key_id = private_key_id

    @property
    def passphrase(self):
        """Gets the passphrase of this PrivateKey.  # noqa: E501


        :return: The passphrase of this PrivateKey.  # noqa: E501
        :rtype: str
        """
        return self._passphrase

    @passphrase.setter
    def passphrase(self, passphrase):
        """Sets the passphrase of this PrivateKey.


        :param passphrase: The passphrase of this PrivateKey.  # noqa: E501
        :type: str
        """

        self._passphrase = passphrase

    @property
    def data(self):
        """Gets the data of this PrivateKey.  # noqa: E501


        :return: The data of this PrivateKey.  # noqa: E501
        :rtype: str
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this PrivateKey.


        :param data: The data of this PrivateKey.  # noqa: E501
        :type: str
        """

        self._data = data

    @property
    def bri(self):
        """Gets the bri of this PrivateKey.  # noqa: E501


        :return: The bri of this PrivateKey.  # noqa: E501
        :rtype: str
        """
        return self._bri

    @bri.setter
    def bri(self, bri):
        """Sets the bri of this PrivateKey.


        :param bri: The bri of this PrivateKey.  # noqa: E501
        :type: str
        """

        self._bri = bri

    @property
    def fingerprint(self):
        """Gets the fingerprint of this PrivateKey.  # noqa: E501


        :return: The fingerprint of this PrivateKey.  # noqa: E501
        :rtype: str
        """
        return self._fingerprint

    @fingerprint.setter
    def fingerprint(self, fingerprint):
        """Sets the fingerprint of this PrivateKey.


        :param fingerprint: The fingerprint of this PrivateKey.  # noqa: E501
        :type: str
        """

        self._fingerprint = fingerprint

    @property
    def updated_at(self):
        """Gets the updated_at of this PrivateKey.  # noqa: E501


        :return: The updated_at of this PrivateKey.  # noqa: E501
        :rtype: str
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this PrivateKey.


        :param updated_at: The updated_at of this PrivateKey.  # noqa: E501
        :type: str
        """

        self._updated_at = updated_at

    @property
    def created_at(self):
        """Gets the created_at of this PrivateKey.  # noqa: E501


        :return: The created_at of this PrivateKey.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this PrivateKey.


        :param created_at: The created_at of this PrivateKey.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def expires_at(self):
        """Gets the expires_at of this PrivateKey.  # noqa: E501


        :return: The expires_at of this PrivateKey.  # noqa: E501
        :rtype: str
        """
        return self._expires_at

    @expires_at.setter
    def expires_at(self, expires_at):
        """Sets the expires_at of this PrivateKey.


        :param expires_at: The expires_at of this PrivateKey.  # noqa: E501
        :type: str
        """

        self._expires_at = expires_at

    @property
    def rescinded(self):
        """Gets the rescinded of this PrivateKey.  # noqa: E501


        :return: The rescinded of this PrivateKey.  # noqa: E501
        :rtype: bool
        """
        return self._rescinded

    @rescinded.setter
    def rescinded(self, rescinded):
        """Sets the rescinded of this PrivateKey.


        :param rescinded: The rescinded of this PrivateKey.  # noqa: E501
        :type: bool
        """

        self._rescinded = rescinded

    @property
    def user_supplied(self):
        """Gets the user_supplied of this PrivateKey.  # noqa: E501


        :return: The user_supplied of this PrivateKey.  # noqa: E501
        :rtype: bool
        """
        return self._user_supplied

    @user_supplied.setter
    def user_supplied(self, user_supplied):
        """Sets the user_supplied of this PrivateKey.


        :param user_supplied: The user_supplied of this PrivateKey.  # noqa: E501
        :type: bool
        """

        self._user_supplied = user_supplied

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
        if issubclass(PrivateKey, dict):
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
        if not isinstance(other, PrivateKey):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
