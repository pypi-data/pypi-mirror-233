"""
Exceptions for the config module
"""


class ConfigException(Exception):
    """Base exception for all config related exceptions"""


class EncryptionKeyNotSetException(ConfigException):
    """Exception to be raised when encryption key is not set"""


class ConfigNotRegisteredException(ConfigException):
    """Exception to be raised when config is not registered"""
