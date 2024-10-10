from .. import Base
from entities.arp import ARPEntity, ARPTag
from sqlalchemy.orm import relationship, backref
from models.router_scan.functions import ARPFunctions
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class ARP(Base):
    __tablename__ = 'arp'  

    arp_id = Column(Integer, primary_key=True, nullable=False)  
    fk_ip_address_id = Column(Integer, ForeignKey('ip_segment.ip_segment_id'), nullable=False)  
    arp_ip = Column(String(15), nullable=False)  
    arp_mac = Column(String(17), nullable=False)  
    arp_alias = Column(String(255), nullable=True)  
    arp_interface = Column(String(255), nullable=False)  
    arp_is_dhcp = Column(Boolean, nullable=False)  
    arp_is_invalid = Column(Boolean, nullable=False)  
    arp_is_dynamic = Column(Boolean, nullable=False)  
    arp_is_complete = Column(Boolean, nullable=False)  
    arp_is_disabled = Column(Boolean, nullable=False)  
    arp_is_published = Column(Boolean, nullable=False)  

    ip_segment = relationship('IPSegment', backref=backref('arp', lazy=True))  

    def __repr__(self):
        return f'<ARP {self.arp_id}>'  

    def to_dict(self):
        return {
            'arp_id': self.arp_id,  
            'fk_ip_address_id': self.fk_ip_address_id,  
            'arp_ip': self.arp_ip,  
            'arp_mac': self.arp_mac,  
            'arp_alias': self.arp_alias,  
            'arp_interface': self.arp_interface,  
            'arp_is_dhcp': self.arp_is_dhcp,  
            'arp_is_invalid': self.arp_is_invalid,  
            'arp_is_dynamic': self.arp_is_dynamic,  
            'arp_is_complete': self.arp_is_complete,  
            'arp_is_disabled': self.arp_is_disabled,  
            'arp_is_published': self.arp_is_published  
        }

    @staticmethod
    def add_arp(session, arp: ARPEntity):
        try:
            if (ARPFunctions.validate_arp_exists(
                session,
                arp.arp_ip,  
                arp.arp_mac  
            )):
                arp.validate_arp()  
                arp_obj = ARP(  
                    fk_ip_address_id=arp.fk_ip_address_id,  
                    arp_ip=arp.arp_ip,  
                    arp_mac=arp.arp_mac,  
                    arp_alias=arp.arp_alias,  
                    arp_interface=arp.arp_interface,  
                    arp_is_dhcp=arp.arp_is_dhcp,  
                    arp_is_invalid=arp.arp_is_invalid,  
                    arp_is_dynamic=arp.arp_is_dynamic,  
                    arp_is_complete=arp.arp_is_complete,  
                    arp_is_disabled=arp.arp_is_disabled,  
                    arp_is_published=arp.arp_is_published  
                )
                session.add(arp_obj)
            else:
                arp.validate_arp()  
                arp_obj = session.query(ARP).filter(
                    ARP.arp_ip == arp.arp_ip,
                    ARP.arp_mac == arp.arp_mac
                ).first()
                arp_obj.fk_ip_address_id = arp.fk_ip_address_id  
                arp_obj.arp_alias = arp.arp_alias  
                arp_obj.arp_interface = arp.arp_interface  
                arp_obj.arp_is_dhcp = arp.arp_is_dhcp  
                arp_obj.arp_is_invalid = arp.arp_is_invalid  
                arp_obj.arp_is_dynamic = arp.arp_is_dynamic  
                arp_obj.arp_is_complete = arp.arp_is_complete  
                arp_obj.arp_is_disabled = arp.arp_is_disabled  
                arp_obj.arp_is_published = arp.arp_is_published
        except Exception as e:  
            raise e

    @staticmethod
    def bulk_add_arp(session, arps: list[ARPEntity]) -> None:
        """
        Bulk add ARP objects to the database
        :param session: Database session
        :param arps: List of ARP objects to add to the database
        :return: None
        """

        try:
            # Create a list of ARP objects obtained from the router
            bulk_list = [ARP(
                fk_ip_address_id=arp.fk_ip_address_id,
                arp_ip=arp.arp_ip,
                arp_mac=arp.arp_mac,
                arp_alias=arp.arp_alias,
                arp_interface=arp.arp_interface,
                arp_is_dhcp=arp.arp_is_dhcp,
                arp_is_invalid=arp.arp_is_invalid,
                arp_is_dynamic=arp.arp_is_dynamic,
                arp_is_complete=arp.arp_is_complete,
                arp_is_disabled=arp.arp_is_disabled,
                arp_is_published=arp.arp_is_published
            ) for arp in arps]

            # Create a list of ARP objects to add to the database
            to_add = []

            # Iterate on the bulk list and check if the ARP object already exists in the database
            for arp in bulk_list:
                # Verify if the ARP object already exists in the database, based on the IP and MAC address
                if (ARPFunctions.validate_arp_exists(
                    session,
                    arp.arp_ip,
                    arp.arp_mac
                )):
                    # If the ARP object does not exist in the database, add it to the list of objects to add
                    to_add.append(arp)
                else:
                    # If it exists, update the ARP object in the database

                    # Get the ARP object from the database
                    arp_obj = session.query(ARP).filter(
                        ARP.arp_ip == arp.arp_ip,
                        ARP.arp_mac == arp.arp_mac
                    ).first()

                    # Update the ARP object with the new values
                    arp_obj.fk_ip_address_id = arp.fk_ip_address_id
                    arp_obj.arp_alias = arp.arp_alias
                    arp_obj.arp_interface = arp.arp_interface
                    arp_obj.arp_is_dhcp = arp.arp_is_dhcp
                    arp_obj.arp_is_invalid = arp.arp_is_invalid
                    arp_obj.arp_is_dynamic = arp.arp_is_dynamic
                    arp_obj.arp_is_complete = arp.arp_is_complete
                    arp_obj.arp_is_disabled = arp.arp_is_disabled
                    arp_obj.arp_is_published = arp.arp_is_published

            # If there are ARP objects to add, add them to the database
            if to_add:
                session.bulk_save_objects(to_add)
        except Exception as e:
            raise e

    @staticmethod
    def delete_arp(session, arp_id):
        try:
            arp = session.query(ARP).get(arp_id)
            arp_tags = session.query(ARPTags).filter(ARPTags.fk_arp_id == arp_id).all()

            for arp_tag in arp_tags:
                session.delete(arp_tag)

            session.delete(arp)
        except Exception as e:  
            raise e

    @staticmethod
    def bulk_delete_arps(session, arp_ids):
        from models.router_scan.models import ARPTags

        model = ARP
        v_arp = ARPFunctions()
        try:
            if v_arp.validate_bulk_delete(session, model, arp_ids):
                session.query(ARPTags).filter(ARPTags.fk_arp_id.in_(arp_ids)).delete(synchronize_session='fetch')
                session.query(ARP).filter(ARP.arp_id.in_(arp_ids)).delete(synchronize_session='fetch')
        except Exception as e:
            raise e

    @staticmethod
    def delete_all_arps(session):
        try:
            session.query(ARPTags).delete()
            session.query(ARP).delete()
        except Exception as e:  
            raise e

    @staticmethod
    def get_arp(session, arp_id):
        try:  
            arp = session.query(ARP).get(arp_id)
            obj = ARPEntity(  
                arp_id=arp.arp_id,  
                fk_ip_address_id=arp.fk_ip_address_id,  
                arp_ip=arp.arp_ip,  
                arp_mac=arp.arp_mac,  
                arp_alias=arp.arp_alias,  
                arp_interface=arp.arp_interface,  
                arp_is_dhcp=arp.arp_is_dhcp,  
                arp_is_invalid=arp.arp_is_invalid,  
                arp_is_dynamic=arp.arp_is_dynamic,  
                arp_is_complete=arp.arp_is_complete,  
                arp_is_disabled=arp.arp_is_disabled,  
                arp_is_published=arp.arp_is_published  
            )
            return obj  
        except Exception as e:  
            raise e

    @staticmethod
    def get_arps(session):
        try:  
            arps = session.query(ARP).all()
            obj_list = []  
            for arp in arps:  
                obj = ARPEntity(  
                    arp_id=arp.arp_id,  
                    fk_ip_address_id=arp.fk_ip_address_id,  
                    arp_ip=arp.arp_ip,  
                    arp_mac=arp.arp_mac,  
                    arp_alias=arp.arp_alias,  
                    arp_interface=arp.arp_interface,  
                    arp_is_dhcp=arp.arp_is_dhcp,  
                    arp_is_invalid=arp.arp_is_invalid,  
                    arp_is_dynamic=arp.arp_is_dynamic,  
                    arp_is_complete=arp.arp_is_complete,  
                    arp_is_disabled=arp.arp_is_disabled,  
                    arp_is_published=arp.arp_is_published  
                )
                obj_list.append(obj)  
            return obj_list  
        except Exception as e:  
            raise e

    @staticmethod
    def get_segment(session, segment_id) -> str:
        try:
            from models.ip_management.models import IPSegment
            segment = session.query(IPSegment).get(segment_id)
            return f'{segment.ip_segment_ip}/{segment.ip_segment_mask}'
        except Exception as e:
            raise e

class ARPTags(Base):
    __tablename__ = 'arp_tag'  

    arp_tag_id = Column(Integer, primary_key=True, nullable=False)  
    fk_arp_id = Column(Integer, ForeignKey('arp.arp_id'), nullable=False)  
    arp_tag_value = Column(String(255), nullable=False)
    
    arp = relationship('ARP', backref=backref('arp_tag', lazy=True))  

    def __repr__(self):
        return f'<ARPTag {self.arp_tag_id}>'  

    def to_dict(self):
        return {
            'arp_tag_id': self.arp_tag_id,  
            'fk_arp_id': self.fk_arp_id,  
            'arp_tag_value': self.arp_tag_value  
        }

    @staticmethod
    def add_arp_tag(session, arp_tag: ARPTag):
        try:
            if (session.query(ARPTags).filter(
                ARPTags.fk_arp_id == arp_tag.fk_arp_id,  
                ARPTags.arp_tag_value == arp_tag.arp_tag_value  
            ).first() is None):
                arp_tag_obj = ARPTags(  
                    fk_arp_id=arp_tag.fk_arp_id,  
                    arp_tag_value=arp_tag.arp_tag_value  
                )
                session.add(arp_tag_obj)
        except Exception as e:  
            raise e

    @staticmethod
    def delete_arp_tag(session, arp_tag_id):
        try:  
            arp_tag = session.query(ARPTags).get(arp_tag_id)
            session.delete(arp_tag)
        except Exception as e:  
            raise e

    @staticmethod
    def delete_all_arp_tags(session):
        try:  
            session.query(ARPTags).delete()
        except Exception as e:
            raise e

    @staticmethod
    def delete_arp_tags(session, arp_id):
        try:  
            session.query(ARPTags).filter(ARPTags.fk_arp_id == arp_id).delete()
        except Exception as e:  
            raise e

    @staticmethod
    def get_arp_tags(session, arp_id):
        try:  
            arp_tags = session.query(ARPTags).filter(ARPTags.fk_arp_id == arp_id).all()
            obj_list = []  
            for arp_tag in arp_tags:  
                obj_list.append(arp_tag.arp_tag_value)  
            return obj_list  
        except Exception as e:  
            raise e

    @staticmethod
    def assign_first_tag(session) -> None:
        """
        Assign the first tag to the ARP objects
        :param session: Database session
        :return: None
        """

        try:
            # Create a list of ARP objects to add
            to_add = []

            # Get available ARP tags defined in the system
            arp_item = None
            arp_tags = ARPTag.get_tags()

            # Get all ARP objects from the database
            arps = session.query(ARP).all()

            # Iterate on the ARP objects and assign the first tag to each ARP object
            for arp in arps:
                unused = True
                # Verify if the ARP object has any tags assigned
                if arp.arp_ip.startswith("10."):
                    # Check if the ARP object already has a internal connection tag or private IP tag
                    if session.query(ARPTags).filter(
                            ARPTags.fk_arp_id == arp.arp_id, ARPTags.arp_tag_value == arp_tags['INTERNAL_CONNECTION']
                                                             or ARPTags.arp_tag_value == arp_tags['PRIVATE_IP']
                    ).first() is None:
                        # Because it is an internal connection, assign the INTERNAL_CONNECTION tag and the PRIVATE_IP tag
                        arp_temp = ARPTags(
                            arp_tag_id=int(),
                            fk_arp_id=arp.arp_id,
                            arp_tag_value=arp_tags['INTERNAL_CONNECTION']
                        )
                        to_add.append(arp_temp)
                        arp_item = arp_tags['PRIVATE_IP']
                        unused = False
                else:
                    # Check if the ARP object already has a external connection tag or public IP tag
                    if session.query(ARPTags).filter(
                            ARPTags.fk_arp_id == arp.arp_id, ARPTags.arp_tag_value == arp_tags['PUBLIC_IP']
                    ).first() is None:
                        # Because it is an external connection, assign the PUBLIC_IP tag
                        arp_item = arp_tags['PUBLIC_IP']
                        unused = False

                if unused is False:
                    # Otherwise, assign the missing tag to the ARP object
                    arp_tag = ARPTags(
                        arp_tag_id=int(),
                        fk_arp_id=arp.arp_id,
                        arp_tag_value=arp_item
                    )
                    to_add.append(arp_tag)

            if to_add is not None:
                # If there are ARP tags to add, add them to the database
                session.bulk_save_objects(to_add)
        except Exception as e:
            raise e
