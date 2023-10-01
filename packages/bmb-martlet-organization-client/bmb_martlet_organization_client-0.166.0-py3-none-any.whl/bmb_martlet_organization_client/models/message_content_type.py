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

class MessageContentType(object):
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
        'id': 'str',
        'name': 'str',
        'organization_id': 'str',
        'b64_schema': 'str',
        'visibility': 'list[str]'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'organization_id': 'organization_id',
        'b64_schema': 'b64_schema',
        'visibility': 'visibility'
    }

    def __init__(self, id=None, name=None, organization_id=None, b64_schema=None, visibility=None):  # noqa: E501
        """MessageContentType - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._organization_id = None
        self._b64_schema = None
        self._visibility = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if organization_id is not None:
            self.organization_id = organization_id
        if b64_schema is not None:
            self.b64_schema = b64_schema
        if visibility is not None:
            self.visibility = visibility

    @property
    def id(self):
        """Gets the id of this MessageContentType.  # noqa: E501

        READ ONLY. Will be generated by the system when creating a new MCT.   # noqa: E501

        :return: The id of this MessageContentType.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this MessageContentType.

        READ ONLY. Will be generated by the system when creating a new MCT.   # noqa: E501

        :param id: The id of this MessageContentType.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this MessageContentType.  # noqa: E501

        REQUIRED. Include +xml or +json as a name component.   # noqa: E501

        :return: The name of this MessageContentType.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MessageContentType.

        REQUIRED. Include +xml or +json as a name component.   # noqa: E501

        :param name: The name of this MessageContentType.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def organization_id(self):
        """Gets the organization_id of this MessageContentType.  # noqa: E501

        READ ONLY. When creating a new MCT the organization_id is taken from the context part of the URL.   # noqa: E501

        :return: The organization_id of this MessageContentType.  # noqa: E501
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this MessageContentType.

        READ ONLY. When creating a new MCT the organization_id is taken from the context part of the URL.   # noqa: E501

        :param organization_id: The organization_id of this MessageContentType.  # noqa: E501
        :type: str
        """

        self._organization_id = organization_id

    @property
    def b64_schema(self):
        """Gets the b64_schema of this MessageContentType.  # noqa: E501

        OPTIONAL. The base64 encoded represenation of the schema. The name of the schema should include +xml or +json and the encoded bytes attached here should be xml, json accordingly. If not supplied the system will provide a minimum schema in xml or json depending on the +xml or +json designation in the name field.   # noqa: E501

        :return: The b64_schema of this MessageContentType.  # noqa: E501
        :rtype: str
        """
        return self._b64_schema

    @b64_schema.setter
    def b64_schema(self, b64_schema):
        """Sets the b64_schema of this MessageContentType.

        OPTIONAL. The base64 encoded represenation of the schema. The name of the schema should include +xml or +json and the encoded bytes attached here should be xml, json accordingly. If not supplied the system will provide a minimum schema in xml or json depending on the +xml or +json designation in the name field.   # noqa: E501

        :param b64_schema: The b64_schema of this MessageContentType.  # noqa: E501
        :type: str
        """

        self._b64_schema = b64_schema

    @property
    def visibility(self):
        """Gets the visibility of this MessageContentType.  # noqa: E501

        OPTIONAL. A list of the organization BRIs able to see this message content type. The owning organization does not need to be included in this list. Including it anyway is not harmful. The system will add it if not present. If no visibility is specified, it will default to bmbix://organization/*, ie public by default.   # noqa: E501

        :return: The visibility of this MessageContentType.  # noqa: E501
        :rtype: list[str]
        """
        return self._visibility

    @visibility.setter
    def visibility(self, visibility):
        """Sets the visibility of this MessageContentType.

        OPTIONAL. A list of the organization BRIs able to see this message content type. The owning organization does not need to be included in this list. Including it anyway is not harmful. The system will add it if not present. If no visibility is specified, it will default to bmbix://organization/*, ie public by default.   # noqa: E501

        :param visibility: The visibility of this MessageContentType.  # noqa: E501
        :type: list[str]
        """

        self._visibility = visibility

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
        if issubclass(MessageContentType, dict):
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
        if not isinstance(other, MessageContentType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
