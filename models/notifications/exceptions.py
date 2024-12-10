"""
This file contains the custom exceptions for the notifications app.

Classes:
    BaseCustomError: Base class for custom exceptions
    NotificationError: Generated when an error occurs with the Notification
    NotificationNotFoundError: Generated when a Notification is not found
    NotNotificationsToRestoreError: Generated when there are no notifications to restore
    NotNotificationsToArchiveError: Generated when there are no notifications to archive
    NotNotificationsToDeleteError: Generated when there are no notifications to delete
"""

# Base class for custom exceptions
class BaseCustomError(Exception):
    """
    Base class for custom exceptions
    """
    pass

class NotificationError(BaseCustomError):
    """
    Generated when an error occurs with the Notification
    """
    def __init__(self, message="An error occurred with the Notification") -> None:
        """
        Constructor for NotificationError
        :param message: Error message
        :type message: str
        """
        self.message = message
        super().__init__(self.message)

class NotificationNotFoundError(BaseCustomError):
    """
    Generated when a Notification is not found
    """
    def __init__(self, message="Notification not found") -> None:
        """
        Constructor for NotificationNotFoundError
        :param message: Error message
        :type message: str
        """
        self.message = message
        super().__init__(self.message)

class NotNotificationsToRestoreError(BaseCustomError):
    """
    Generated when there are no notifications to restore
    """
    def __init__(self, message="There are no notifications to restore") -> None:
        """
        Constructor for NotNotificationsToRestoreError
        :param message: Error message
        :type message: str
        """
        self.message = message
        super().__init__(self.message)

class NotNotificationsToArchiveError(BaseCustomError):
    """
    Generated when there are no notifications to archive
    """
    def __init__(self, message="There are no notifications to archive") -> None:
        """
        Constructor for NotNotificationsToArchiveError
        :param message: Error message
        :type message: str
        """
        self.message = message
        super().__init__(self.message)

class NotNotificationsToDeleteError(BaseCustomError):
    """
    Generated when there are no notifications to delete
    """
    def __init__(self, message="There are no notifications to delete") -> None:
        """
        Constructor for NotNotificationsToDeleteError
        :param message: Error message
        :type message: str
        """
        self.message = message
        super().__init__(self.message)
