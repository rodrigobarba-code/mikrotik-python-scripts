# Description: IP Addresses Model for the IP Addresses Blueprint

# Importing Required Libraries
from sqlalchemy import Enum
from app.extensions import db
# Importing Required Libraries

# Importing Required Entities
from app.blueprints.ip_management.entities import IPSegmentTag, IPSegmentEntity
# Importing Required Entities

# Importing Required Models
from app.blueprints.routers.models import Router
# Importing Required Models

# Importing Required Functions
from app.blueprints.ip_management.functions import IPAddressesFunctions
# Importing Required Functions

# IP Segment Model
class IPSegment(db.Model):
    __tablename__ = 'ip_segment'  # Table Name

    # Columns
    ip_segment_id = db.Column(db.Integer, primary_key=True, nullable=False)  # IP Segment ID
    fk_router_id = db.Column(db.Integer, db.ForeignKey('routers.router_id'), nullable=False)  # FK Router ID
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
    def add_ip_segment(ip_segment: IPSegmentEntity):
        try:  # Try to add the IP Segment
            # If the IP Segment is new and does not exist
            if (IPAddressesFunctions.validate_ip_segment_exists(
                ip_segment.ip_segment_ip,
                ip_segment.ip_segment_mask,
                ip_segment.ip_segment_interface
            )):
                # If the segment does not exist, add it
                ip_segment.validate_ip_segment()  # Validate the IP Segment
                ip_segment_obj = IPSegment(  # Create the IP Segment Object for Database Insertion
                    fk_router_id=ip_segment.fk_router_id,  # FK Router ID
                    ip_segment_ip=ip_segment.ip_segment_ip,  # IP Segment IP
                    ip_segment_mask=ip_segment.ip_segment_mask,  # IP Segment Mask
                    ip_segment_network=ip_segment.ip_segment_network,  # IP Segment Network
                    ip_segment_interface=ip_segment.ip_segment_interface,  # IP Segment Interface
                    ip_segment_actual_iface=ip_segment.ip_segment_actual_iface,  # IP Segment Actual Interface
                    ip_segment_tag=ip_segment.ip_segment_tag,  # IP Segment Tag
                    ip_segment_comment=ip_segment.ip_segment_comment,  # IP Segment Comment
                    ip_segment_is_invalid=ip_segment.ip_segment_is_invalid,  # IP Segment Is Invalid
                    ip_segment_is_dynamic=ip_segment.ip_segment_is_dynamic,  # IP Segment Is Dynamic
                    ip_segment_is_disabled=ip_segment.ip_segment_is_disabled  # IP Segment Is Disabled
                )
                db.session.add(ip_segment_obj)  # Add the IP Segment Object to the Database Session
                db.session.commit()  # Commit the Database Session
            # If already exists, update all the fields
            else:
                ip_segment.validate_ip_segment()  # Validate the IP Segment
                ip_segment_obj = IPSegment.query.filter(
                    IPSegment.ip_segment_ip == ip_segment.ip_segment_ip,  # IP Segment IP
                    IPSegment.ip_segment_mask == ip_segment.ip_segment_mask,  # IP Segment Mask
                    IPSegment.ip_segment_interface == ip_segment.ip_segment_interface  # IP Segment Interface
                ).first()
                ip_segment_obj.fk_router_id = ip_segment.fk_router_id  # FK Router ID
                ip_segment_obj.ip_segment_network = ip_segment.ip_segment_network  # IP Segment Network
                ip_segment_obj.ip_segment_interface = ip_segment.ip_segment_interface  # IP Segment Interface
                ip_segment_obj.ip_segment_actual_iface = ip_segment.ip_segment_actual_iface  # IP Segment Actual Interface
                ip_segment_obj.ip_segment_tag = ip_segment.ip_segment_tag  # IP Segment Tag
                ip_segment_obj.ip_segment_comment = ip_segment.ip_segment_comment  # IP Segment Comment
                ip_segment_obj.ip_segment_is_invalid = ip_segment.ip_segment_is_invalid  # IP Segment Is Invalid
                ip_segment_obj.ip_segment_is_dynamic = ip_segment.ip_segment_is_dynamic  # IP Segment Is Dynamic
                ip_segment_obj.ip_segment_is_disabled = ip_segment.ip_segment_is_disabled  # IP Segment Is Disabled
                db.session.commit()  # Commit the Database Session
        except Exception as e:  # If an Exception occurs
            db.session.rollback()  # Rollback the Database Session
            print(e)
    # IP Segment - Add IP Segment

    # IP Segment - Delete IP Segment
    @staticmethod
    def delete_ip_segment(ip_segment_id):
        try:  # Try to delete the IP Segment
            ip_segment = IPSegment.query.get(ip_segment_id)  # Get the IP Segment
            db.session.delete(ip_segment)  # Delete the IP Segment
            db.session.commit()  # Commit the Database Session
        except Exception as e:  # If an Exception occurs
            db.session.rollback()  # Rollback the Database Session
            print(e)
    # IP Segment - Delete IP Segment

    # Ip Segment - Delete All IP Segments
    @staticmethod
    def delete_all_ip_segments():
        try:  # Try to delete all IP Segments
            IPSegment.query.delete()  # Delete all IP Segments
            db.session.commit()  # Commit the Database Session
        except Exception as e:
            db.session.rollback()
            print(e)
    # Ip Segment - Delete All IP Segments

    # IP Segment - Get IP Segment
    @staticmethod
    def get_ip_segment(ip_segment_id):
        try:  # Try to get the IP Segment
            ip_segment = IPSegment.query.get(ip_segment_id)  # Get the IP Segment
            obj = IPSegmentEntity(  # Create an instance of the IPSegmentEntity class
                ip_segment_id=ip_segment.ip_segment_id,  # IP Segment ID
                fk_router_id=ip_segment.fk_router_id,  # FK Router ID
                ip_segment_ip=ip_segment.ip_segment_ip,  # IP Segment IP
                ip_segment_mask=ip_segment.ip_segment_mask,  # IP Segment Mask
                ip_segment_network=ip_segment.ip_segment_network,  # IP Segment Network
                ip_segment_interface=ip_segment.ip_segment_interface,  # IP Segment Interface
                ip_segment_actual_iface=ip_segment.ip_segment_actual_iface,  # IP Segment Actual Interface
                ip_segment_tag=ip_segment.ip_segment_tag,  # IP Segment Tag
                ip_segment_comment=ip_segment.ip_segment_comment,  # IP Segment Comment
                ip_segment_is_invalid=ip_segment.ip_segment_is_invalid,  # IP Segment Is Invalid
                ip_segment_is_dynamic=ip_segment.ip_segment_is_dynamic,  # IP Segment Is Dynamic
                ip_segment_is_disabled=ip_segment.ip_segment_is_disabled  # IP Segment Is Disabled
            )
            return obj  # Return the IP Segment Entity
        except Exception as e:  # If an Exception occurs
            print(e)
    # IP Segment - Get IP Segment

    # IP Segment - Get IP Segments
    @staticmethod
    def get_ip_segments():
        try:  # Try to get the IP Segments
            ip_segments = IPSegment.query.all()  # Get all the IP Segments
            ip_segment_list = []  # IP Segment List
            for ip_segment in ip_segments:  # For each IP Segment
                obj = IPSegmentEntity(  # Create an instance of the IPSegmentEntity class
                    ip_segment_id=ip_segment.ip_segment_id,  # IP Segment ID
                    fk_router_id=ip_segment.fk_router_id,  # FK Router ID
                    ip_segment_ip=ip_segment.ip_segment_ip,  # IP Segment IP
                    ip_segment_mask=ip_segment.ip_segment_mask,  # IP Segment Mask
                    ip_segment_network=ip_segment.ip_segment_network,  # IP Segment Network
                    ip_segment_interface=ip_segment.ip_segment_interface,  # IP Segment Interface
                    ip_segment_actual_iface=ip_segment.ip_segment_actual_iface,  # IP Segment Actual Interface
                    ip_segment_tag=ip_segment.ip_segment_tag,  # IP Segment Tag
                    ip_segment_comment=ip_segment.ip_segment_comment,  # IP Segment Comment
                    ip_segment_is_invalid=ip_segment.ip_segment_is_invalid,  # IP Segment Is Invalid
                    ip_segment_is_dynamic=ip_segment.ip_segment_is_dynamic,  # IP Segment Is Dynamic
                    ip_segment_is_disabled=ip_segment.ip_segment_is_disabled  # IP Segment Is Disabled
                )
                ip_segment_list.append(obj)  # Append the IP Segment Entity to the IP Segment List
            return ip_segment_list  # Return the IP Segment List
        except Exception as e:  # If an Exception occurs
            print(e)
    # IP Segment - Get IP Segments

    # IP Segment - Get IP Segments by Site ID
    @staticmethod
    def get_ip_segments_by_site_id(site_id):
        try:  # Try to get the IP Segments
            router = Router.query.filter_by(fk_site_id=site_id).first()  # Get the Router
            ip_segments = IPSegment.query.filter_by(fk_router_id=router.router_id).all()  # Get all the IP Segments
            ip_segment_list = []  # IP Segment List
            for ip_segment in ip_segments:  # For each IP Segment
                obj = IPSegmentEntity(  # Create an instance of the IPSegmentEntity class
                    ip_segment_id=ip_segment.ip_segment_id,  # IP Segment ID
                    fk_router_id=ip_segment.fk_router_id,  # FK Router ID
                    ip_segment_ip=ip_segment.ip_segment_ip,  # IP Segment IP
                    ip_segment_mask=ip_segment.ip_segment_mask,  # IP Segment Mask
                    ip_segment_network=ip_segment.ip_segment_network,  # IP Segment Network
                    ip_segment_interface=ip_segment.ip_segment_interface,  # IP Segment Interface
                    ip_segment_actual_iface=ip_segment.ip_segment_actual_iface,  # IP Segment Actual Interface
                    ip_segment_tag=ip_segment.ip_segment_tag,  # IP Segment Tag
                    ip_segment_comment=ip_segment.ip_segment_comment,  # IP Segment Comment
                    ip_segment_is_invalid=ip_segment.ip_segment_is_invalid,  # IP Segment Is Invalid
                    ip_segment_is_dynamic=ip_segment.ip_segment_is_dynamic,  # IP Segment Is Dynamic
                    ip_segment_is_disabled=ip_segment.ip_segment_is_disabled  # IP Segment Is Disabled
                )
                ip_segment_list.append(obj)  # Append the IP Segment Entity to the IP Segment List
            return ip_segment_list  # Return the IP Segment List
        except Exception as e:  # If an Exception occurs
            print(e)
    # IP Segment - Get IP Segments by Site ID

    # IP Segment - Get IP Segments by Router ID
    @staticmethod
    def get_ip_segments_by_router_id(router_id):
        try:  # Try to get the IP Segments
            ip_segments = IPSegment.query.filter_by(fk_router_id=router_id).all()  # Get all the IP Segments
            ip_segment_list = []  # IP Segment List
            for ip_segment in ip_segments:  # For each IP Segment
                obj = IPSegmentEntity(  # Create an instance of the IPSegmentEntity class
                    ip_segment_id=ip_segment.ip_segment_id,  # IP Segment ID
                    fk_router_id=ip_segment.fk_router_id,  # FK Router ID
                    ip_segment_ip=ip_segment.ip_segment_ip,  # IP Segment IP
                    ip_segment_mask=ip_segment.ip_segment_mask,  # IP Segment Mask
                    ip_segment_network=ip_segment.ip_segment_network,  # IP Segment Network
                    ip_segment_interface=ip_segment.ip_segment_interface,  # IP Segment Interface
                    ip_segment_actual_iface=ip_segment.ip_segment_actual_iface,  # IP Segment Actual Interface
                    ip_segment_tag=ip_segment.ip_segment_tag,  # IP Segment Tag
                    ip_segment_comment=ip_segment.ip_segment_comment,  # IP Segment Comment
                    ip_segment_is_invalid=ip_segment.ip_segment_is_invalid,  # IP Segment Is Invalid
                    ip_segment_is_dynamic=ip_segment.ip_segment_is_dynamic,  # IP Segment Is Dynamic
                    ip_segment_is_disabled=ip_segment.ip_segment_is_disabled  # IP Segment Is Disabled
                )
                ip_segment_list.append(obj)  # Append the IP Segment Entity to the IP Segment List
            return ip_segment_list  # Return the IP Segment List
        except Exception as e:  # If an Exception occurs
            print(e)
    # IP Segment - Get IP Segments by Router ID
    # Static Methods
# IP Segment Model
