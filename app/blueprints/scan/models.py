# Description: Scan Model for the Scan Blueprint

# Importing Required Libraries
from sqlalchemy import Enum
from app.extensions import db
from app.extensions import func
# Importing Required Libraries

# Importing Required Entities
from app.blueprints.scan.entities import ARPEntity, ARPTag
# Importing Required Entities

# Importing Required Exceptions
from app.blueprints.scan.exceptions import *
# Importing Required Exceptions

# ARP Model
class ARP(db.Model):
    __tablename__ = 'arp'  # Table Name

    # Columns
    arp_id = db.Column(db.Integer, primary_key=True, nullable=False)  # ARP ID
    fk_ip_address_id = db.Column(db.Integer, db.ForeignKey('ip_segment.ip_segment_id'), nullable=False)  # FK IP Address ID
    arp_ip = db.Column(db.String(15), nullable=False)  # ARP IP
    arp_mac = db.Column(db.String(17), nullable=False)  # ARP MAC
    arp_tag = db.Column(Enum(ARPTag), nullable=False)  # ARP Tag
    arp_interface = db.Column(db.String(255), nullable=False)  # ARP Interface
    arp_is_dhcp = db.Column(db.Boolean, nullable=False)  # ARP DHCP
    arp_is_invalid = db.Column(db.Boolean, nullable=False)  # ARP Invalid
    arp_is_dynamic = db.Column(db.Boolean, nullable=False)  # ARP Dynamic
    arp_is_complete = db.Column(db.Boolean, nullable=False)  # ARP Complete
    arp_is_disabled = db.Column(db.Boolean, nullable=False)  # ARP Disabled
    arp_is_published = db.Column(db.Boolean, nullable=False)  # ARP Published
    # Columns

    # Relationships
    ip_segment = db.relationship('IPSegment', backref=db.backref('arp', lazy=True))  # IP Segment Relationship
    # Relationships

    # Object Representation
    def __repr__(self):
        return f'<ARP {self.arp_id}>'  # ARP Object Representation
    # Object Representation

    # Dictionary Representation
    def to_dict(self):
        return {
            'arp_id': self.arp_id,  # ARP ID
            'fk_ip_address_id': self.fk_ip_address_id,  # FK IP Address ID
            'arp_ip': self.arp_ip,  # ARP IP
            'arp_mac': self.arp_mac,  # ARP MAC
            'arp_tag': self.arp_tag,  # ARP Tag
            'arp_interface': self.arp_interface,  # ARP Interface
            'arp_is_dhcp': self.arp_is_dhcp,  # ARP DHCP
            'arp_is_invalid': self.arp_is_invalid,  # ARP Invalid
            'arp_is_dynamic': self.arp_is_dynamic,  # ARP Dynamic
            'arp_is_complete': self.arp_is_complete,  # ARP Complete
            'arp_is_disabled': self.arp_is_disabled,  # ARP Disabled
            'arp_is_published': self.arp_is_published  # ARP Published
        }
    # Dictionary Representation

    # Static Methods
    # ARP - Add ARP
    @staticmethod
    def add_arp(arp):
        pass
    # ARP - Add ARP

    # ARP - Delete ARP
    @staticmethod
    def delete_region(arp_id):
        pass
    # ARP - Delete ARP

    # ARP - Get ARP
    @staticmethod
    def get_arp(arp_id):
        pass
    # ARP - Get ARP

    # ARP - Get ARPs
    @staticmethod
    def get_arps():
        pass
    # ARP - Get ARPs
    # Static Methods
# ARP Model
