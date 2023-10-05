"""
UCAPIErr.py

module for custom errors used by UtilityCloudAPIWrapper.py
"""

from requests import RequestException


class InvalidRequestMethod(RequestException):
    ...


class InvalidConfigError(Exception):
    ...


class MissingConfigError(InvalidConfigError):
    ...


class InvalidUtilityCloudUserName(Exception):
    ...


class AuthenticationError(Exception):
    ...
