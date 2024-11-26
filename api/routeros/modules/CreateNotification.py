import datetime
from entities.notification import NotificationEntity
from models.notifications.models import Notification

from utils.threading_manager import ThreadingManager

class CreateNotification:
    """
    Class for Create Notification

    Methods:
        init: Constructor
    """

    # Constructor
    added_ip_segments: int = None
    updated_ip_segments: int = None
    added_ip_groups: int = None
    updated_ip_groups: int = None
    deleted_ip_groups: int = None
    duplicity: int = None

    def __init__(
            self,
            added_ip_segments: int = None,
            updated_ip_segments: int = None,
            added_ip_groups: int = None,
            updated_ip_groups: int = None,
            deleted_ip_groups: int = None,
            duplicity: int = None
    ):
        self.added_ip_segments = added_ip_segments
        self.updated_ip_segments = updated_ip_segments
        self.added_ip_groups = added_ip_groups
        self.updated_ip_groups = updated_ip_groups
        self.deleted_ip_groups = deleted_ip_groups
        self.duplicity = duplicity

    def create_success_notification(self):
        """
        Create Success Notification
        :return: None
        """

        # Get the current date and time
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create a new Notification Entity
        notification = NotificationEntity(
            notification_title='Router Scanning Process Completed Successfully',
            notification_body=
'''Router Scanning Process has been completed successfully.
We found the following:
- Added IP Segments: {added_ip_segments},
- Updated IP Segments: {updated_ip_segments},
- Added IP Groups: {added_ip_groups},
- Updated IP Groups: {updated_ip_groups},
- Deleted IP Groups: {deleted_ip_groups},
- Anomalies: {duplicity}.
The current date and time for this notification is {date}.
Thank you for using our service. Seven Suite Team.'''.format(
                added_ip_segments=self.added_ip_segments,
                updated_ip_segments=self.updated_ip_segments,
                added_ip_groups=self.added_ip_groups,
                updated_ip_groups=self.updated_ip_groups,
                deleted_ip_groups=self.deleted_ip_groups,
                duplicity=self.duplicity,
                date=date
            ),
            notification_type='success',
            notification_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            is_archived=0
        )

        # Validate Notification
        notification.validate()

        # Add Notification
        ThreadingManager().run_thread(
            Notification.add_notification,
            'w',
            notification
        )

    def create_warning_notification(self):
        """
        Create Warning Notification
        :return: None
        """

        # Get the current date and time
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create a new Notification Entity
        notification = NotificationEntity(
            notification_title='Anomalies Found in Router Scanning Process',
            notification_body=
'''The Router Scanning Process has been completed with warnings.
We found there are some anomalies in the process.
With a total of: {duplicity} anomalies. 
(Duplicity generally means that the same IP address is in multiple groups)
The current date and time for this notification is {date}.
Thank you for using our service. Seven Suite Team.'''.format(
                duplicity=self.duplicity,
                date=date
            ),
            notification_type='warning',
            notification_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            is_archived=0
        )

        # Validate Notification
        notification.validate()

        # Add Notification
        ThreadingManager().run_thread(
            Notification.add_notification,
            'w',
            notification
        )

    @staticmethod
    def create_error_notification(error: str):
        """
        Create Error Notification
        :return: None
        """

        # Get the current date and time
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create a new Notification Entity
        notification = NotificationEntity(
            notification_title='Router Scanning Process Failed',
            notification_body=
'''The Router Scanning Process has failed.
There was an error in the process.
Error: {error}.
The current date and time for this notification is {date}.
Please try again later. Seven Suite Team.'''.format(
                error=error,
                date=date
            ),
            notification_type='error',
            notification_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            is_archived=0
        )

        # Validate Notification
        notification.validate()

        # Add Notification
        ThreadingManager().run_thread(
            Notification.add_notification,
            'w',
            notification
        )
