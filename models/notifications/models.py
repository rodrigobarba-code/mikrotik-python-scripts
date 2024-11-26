from app.blueprints.notifications.routes import notifications
from .. import Base
from sqlalchemy import delete, text, update
from sqlalchemy import Column, Integer, String, Enum

from entities.notification import NotificationEntity
from models.notifications.exceptions import NotificationError, NotificationNotFoundError

# Class for Notification Model

class Notification(Base):
    __tablename__ = 'notifications'  # Table Name

    acceptable_types = ['error', 'warning', 'success']  # Acceptable Notification Types

    notification_id = Column(Integer, primary_key=True, autoincrement=True)  # Notification ID
    notification_title = Column(String(128), nullable=False)  # Notification Title
    notification_body = Column(String(512), nullable=False)  # Notification Body
    notification_type = Column(Enum(*acceptable_types), nullable=False)  # Notification Type
    notification_datetime = Column(String(128), nullable=False)  # Notification Datetime
    is_archived = Column(Integer, nullable=False, default=0)  # Is Archived

    def __repr__(self):
        return f'<Notification {self.notification_id}>'  # Return Notification ID

    def to_dict(self):
        return {
            'notification_id': self.notification_id,  # Notification ID
            'notification_title': self.notification_title,  # Notification Title
            'notification_body': self.notification_body,  # Notification Body
            'notification_type': self.notification_type,  # Notification Type
            'notification_datetime': self.notification_datetime,  # Notification Datetime
            'is_archived': self.is_archived  # Is Archived
        }

    @staticmethod
    def verify_autoincrement_id(session) -> None:
        """
        Verify Autoincrement ID
        :param session: Database context session
        :return: None
        """
        try:
            # Check if there are no Notifications
            if not session.query(Notification).all():
                 # Reset Autoincrement ID
                session.execute(text("ALTER TABLE notifications AUTO_INCREMENT = 1"))
        except Exception as e:
            raise NotificationError()

    @staticmethod
    def add_notification(session, notification: NotificationEntity) -> None:
        """
        Add Notification
        :param session: Database context session
        :param notification: Notification Entity
        :return: None
        """
        try:
            notification.validate()  # Validate Notification
            new_notification = Notification(
                notification_title=notification.notification_title,  # Notification Title
                notification_body=notification.notification_body,  # Notification Body
                notification_type=notification.notification_type,  # Notification Type
                notification_datetime=notification.notification_datetime  # Notification Datetime
            )
            session.add(new_notification)  # Add Notification
        except ValueError as e:
            raise NotificationError()

    @staticmethod
    def archive_notification(session, notification_id: int) -> None:
        """
        Archive Notification
        :param session: Database context session
        :param notification_id: Notification ID
        :return: None
        """
        try:
            notification = session.query(Notification).get(notification_id)  # Get Notification
            if not notification:  # Check if Notification is not found
                raise NotificationNotFoundError()
            notification.is_archived = 1  # Archive Notification
        except NotificationNotFoundError as e:
            raise e
        except Exception as e:
            raise NotificationError()

    @staticmethod
    def archive_all_notifications(session) -> None:
        """
        Archive All Notifications
        :param session: Database context session
        :return: None
        """
        try:
            # Check if Notifications are not found
            session.execute(update(Notification).values(is_archived=1))  # Archive All Notifications
        except Exception as e:
            raise NotificationError()

    @staticmethod
    def delete_notification(session, notification_id: int) -> None:
        """
        Delete Notification
        :param session: Database context session
        :param notification_id: Notification ID
        :return: None
        """
        try:
            # Check if Notification is not found
            session.execute(delete(Notification).where(Notification.notification_id == notification_id))  # Delete Notification
        except Exception as e:
            raise NotificationError()

    @staticmethod
    def delete_all_notifications(session) -> None:
        """
        Delete All Notifications
        :param session: Database context session
        :return: None
        """
        try:
            # Check if Notifications are not found
            session.execute(delete(Notification))  # Delete All Notifications
        except Exception as e:
            raise NotificationError()

    @staticmethod
    def get_notifications(session) -> list:
        """
        Get Notifications
        :param session: Database context session
        :return: List of Notifications
        """
        try:
            # Return Notifications
            return [
                NotificationEntity(
                    notification_id=notification.notification_id,  # Notification ID
                    notification_title=notification.notification_title,  # Notification Title
                    notification_body=notification.notification_body,  # Notification Body
                    notification_type=notification.notification_type,  # Notification Type
                    notification_datetime=notification.notification_datetime,  # Notification Datetime
                    is_archived=notification.is_archived  # Is Archived
                )
                for notification in session.query(Notification).all()  # Get Notifications
            ]
        except Exception as e:
            raise NotificationError()

# Class for Notification Model
