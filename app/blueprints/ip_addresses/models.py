# Description: IP Addresses Model for the IP Addresses Blueprint

# Importing Required Libraries
from sqlalchemy import Enum
from app.extensions import db
from app.extensions import func
# Importing Required Libraries

# Importing Required Entities
from app.blueprints.ip_addresses.entities import IPSegmentTag, IPSegmentEntity
# Importing Required Entities

# Importing Required Exceptions
from app.blueprints.scan.exceptions import *
# Importing Required Exceptions

# IP Segment Model
class IPSegment(db.Model):
    __tablename__ = 'ip_segment'  # Table Name

    # Columns
    ip_segment_id = db.Column(db.Integer, primary_key=True, nullable=False)  # IP Segment ID
    fk_router_id = db.Column(db.Integer, db.ForeignKey('router.router_id'), nullable=False)  # FK Router ID
    ip_segment_ip = db.Column(db.String(15), nullable=False)  # IP Segment IP
    ip_segment_mask = db.Column(db.String(15), nullable=False)  # IP Segment Mask
    ip_segment_network = db.Column(db.String(15), nullable=False)  # IP Segment Network
    ip_segment_interface = db.Column(db.String(255), nullable=False)  # IP Segment Interface
    ip_segment_actual_iface = db.Column(db.String(255), nullable=False)  # IP Segment Actual Interface
    ip_segment_tag = db.Column(Enum(IPSegmentTag), nullable=False)  # IP Segment Tag
    ip_segment_comment = db.Column(db.String(255), nullable=False)  # IP Segment Comment
    ip_segment_is_invalid = db.Column(db.Boolean, nullable=False)  # IP Segment Is Invalid
    ip_segment_is_dynamic = db.Column(db.Boolean, nullable=False)  # IP Segment Is Dynamic
    ip_segment_is_disabled = db.Column(db.Boolean, nullable=False)  # IP Segment
    # Columns

    # Object Representation
    def __repr__(self):
        return f'<IP Segment {self.ip_segment_id}>'  # IP Segment Object Representation
    # Object Representation

    # Dictionary Representation
    def to_dict(self):
        return {
            'ip_segment_id': self.ip_segment_id,  # IP Segment ID
            'fk_router_id': self.fk_router_id,  # FK Router ID
            'ip_segment_ip': self.ip_segment_ip,  # IP Segment IP
            'ip_segment_mask': self.ip_segment_mask,  # IP Segment Mask
            'ip_segment_network': self.ip_segment_network,  # IP Segment Network
            'ip_segment_interface': self.ip_segment_interface,  # IP Segment Interface
            'ip_segment_actual_iface': self.ip_segment_actual_iface,  # IP Segment Actual Interface
            'ip_segment_tag': self.ip_segment_tag,  # IP Segment Tag
            'ip_segment_comment': self.ip_segment_comment,  # IP Segment Comment
            'ip_segment_is_invalid': self.ip_segment_is_invalid,  # IP Segment Is Invalid
            'ip_segment_is_dynamic': self.ip_segment_is_dynamic,  # IP Segment Is Dynamic
            'ip_segment_is_disabled': self.ip_segment_is_disabled  # IP Segment Is Disabled
        }
    # Dictionary Representation

    # Static Methods
    # IP Segment - Add IP Segment
    @staticmethod
    def add_ip_segment(ip_segment):
        try:  # Try to add the IP Segment
            db.session.add(ip_segment)  # Add the IP Segment to the database
            db.session.commit()  # Commit the changes
            return ip_segment  # Return the IP Segment
        except Exception as e:  # Catch any exceptions
            db.session.rollback()  # Rollback the changes
            pass  # Pass the exception
    # IP Segment - Add IP Segment

    # IP Segment - Update IP Segment
    @staticmethod
    def update_ip_segment(ip_segment_id, ip_segment):
        pass
    # IP Segment - Update IP Segment

    # IP Segment - Delete IP Segment
    @staticmethod
    def delete_ip_segment(ip_segment_id):
        pass
    # IP Segment - Delete IP Segment

    # IP Segment - Get IP Segment
    @staticmethod
    def get_ip_segment(ip_segment_id):
        pass
    # IP Segment - Get IP Segment

    # IP Segment - Get IP Segments
    @staticmethod
    def get_ip_segments():
        pass
    # IP Segment - Get IP Segments
    # Static Methods
# IP Segment Model
