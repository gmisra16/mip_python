import connexion
import six

from swagger_server import util


def get_airlines(name):  # noqa: E501
    """Finds Airlines by name

    Muliple namess can be provided with comma separated strings. Use name1, name2, name3 for testing. # noqa: E501

    :param name: Names to filter by
    :type name: List[str]

    :rtype: None
    """
    return 'do some magic!'
