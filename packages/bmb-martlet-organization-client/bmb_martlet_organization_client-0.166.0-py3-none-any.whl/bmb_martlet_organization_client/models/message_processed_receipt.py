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

class MessageProcessedReceipt(object):
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
        'message_processed_receipt_id': 'str',
        'received_timestamp': 'str',
        'message_id': 'str',
        'result': 'str',
        'reference': 'str',
        'comments': 'str'
    }

    attribute_map = {
        'message_processed_receipt_id': 'message_processed_receipt_id',
        'received_timestamp': 'received_timestamp',
        'message_id': 'message_id',
        'result': 'result',
        'reference': 'reference',
        'comments': 'comments'
    }

    def __init__(self, message_processed_receipt_id=None, received_timestamp=None, message_id=None, result=None, reference=None, comments=None):  # noqa: E501
        """MessageProcessedReceipt - a model defined in Swagger"""  # noqa: E501
        self._message_processed_receipt_id = None
        self._received_timestamp = None
        self._message_id = None
        self._result = None
        self._reference = None
        self._comments = None
        self.discriminator = None
        if message_processed_receipt_id is not None:
            self.message_processed_receipt_id = message_processed_receipt_id
        if received_timestamp is not None:
            self.received_timestamp = received_timestamp
        if message_id is not None:
            self.message_id = message_id
        if result is not None:
            self.result = result
        if reference is not None:
            self.reference = reference
        if comments is not None:
            self.comments = comments

    @property
    def message_processed_receipt_id(self):
        """Gets the message_processed_receipt_id of this MessageProcessedReceipt.  # noqa: E501


        :return: The message_processed_receipt_id of this MessageProcessedReceipt.  # noqa: E501
        :rtype: str
        """
        return self._message_processed_receipt_id

    @message_processed_receipt_id.setter
    def message_processed_receipt_id(self, message_processed_receipt_id):
        """Sets the message_processed_receipt_id of this MessageProcessedReceipt.


        :param message_processed_receipt_id: The message_processed_receipt_id of this MessageProcessedReceipt.  # noqa: E501
        :type: str
        """

        self._message_processed_receipt_id = message_processed_receipt_id

    @property
    def received_timestamp(self):
        """Gets the received_timestamp of this MessageProcessedReceipt.  # noqa: E501


        :return: The received_timestamp of this MessageProcessedReceipt.  # noqa: E501
        :rtype: str
        """
        return self._received_timestamp

    @received_timestamp.setter
    def received_timestamp(self, received_timestamp):
        """Sets the received_timestamp of this MessageProcessedReceipt.


        :param received_timestamp: The received_timestamp of this MessageProcessedReceipt.  # noqa: E501
        :type: str
        """

        self._received_timestamp = received_timestamp

    @property
    def message_id(self):
        """Gets the message_id of this MessageProcessedReceipt.  # noqa: E501


        :return: The message_id of this MessageProcessedReceipt.  # noqa: E501
        :rtype: str
        """
        return self._message_id

    @message_id.setter
    def message_id(self, message_id):
        """Sets the message_id of this MessageProcessedReceipt.


        :param message_id: The message_id of this MessageProcessedReceipt.  # noqa: E501
        :type: str
        """

        self._message_id = message_id

    @property
    def result(self):
        """Gets the result of this MessageProcessedReceipt.  # noqa: E501


        :return: The result of this MessageProcessedReceipt.  # noqa: E501
        :rtype: str
        """
        return self._result

    @result.setter
    def result(self, result):
        """Sets the result of this MessageProcessedReceipt.


        :param result: The result of this MessageProcessedReceipt.  # noqa: E501
        :type: str
        """

        self._result = result

    @property
    def reference(self):
        """Gets the reference of this MessageProcessedReceipt.  # noqa: E501


        :return: The reference of this MessageProcessedReceipt.  # noqa: E501
        :rtype: str
        """
        return self._reference

    @reference.setter
    def reference(self, reference):
        """Sets the reference of this MessageProcessedReceipt.


        :param reference: The reference of this MessageProcessedReceipt.  # noqa: E501
        :type: str
        """

        self._reference = reference

    @property
    def comments(self):
        """Gets the comments of this MessageProcessedReceipt.  # noqa: E501


        :return: The comments of this MessageProcessedReceipt.  # noqa: E501
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """Sets the comments of this MessageProcessedReceipt.


        :param comments: The comments of this MessageProcessedReceipt.  # noqa: E501
        :type: str
        """

        self._comments = comments

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
        if issubclass(MessageProcessedReceipt, dict):
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
        if not isinstance(other, MessageProcessedReceipt):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
