# Description: Notification Entities

# Class for Notification Entity
class NotificationEntity:
    # Constructor
    def __init__(
        self,
        notification_id: int = 0,  # Notification ID
        notification_title: str = '',  # Notification Title
        notification_body: str = '',  # Notification Body
        notification_type: str = '',  # Notification Type
        notification_datetime: str = '',  # Notification Datetime
        is_archived: int = 0,  # Is Archived
    ):
        self.notification_id = notification_id
        self.notification_title = notification_title
        self.notification_body = notification_body
        self.notification_type = notification_type
        self.notification_datetime = notification_datetime
        self.is_archived = is_archived
    # Constructor

    # Validate Notification Entity
    def validate(self):
        try:
            # Check for each attribute to be valid
            assert isinstance(self.notification_id, int)  # Verify if Notification ID is an Integer
            assert isinstance(self.notification_title, str)  # Verify if Notification Title is a String
            assert isinstance(self.notification_body, str)  # Verify if Notification Body is a String
            assert isinstance(self.notification_type, str)  # Verify if Notification Type is a String
            assert isinstance(self.notification_datetime, str)  # Verify if Notification Datetime is a String
            assert isinstance(self.is_archived, int)  # Verify if Is Archived is an Integer
            # Check for each attribute to be valid
        except AssertionError:
            raise ValueError('Invalid Notification Entity')  # Raise ValueError if Assertion Error
    # Validate Notification Entity
# Class for Notification Entity
