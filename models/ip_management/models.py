from .. import Base
from models.routers.models import Router
from sqlalchemy.orm import relationship, backref
from entities.ip_segment import IPSegmentTag, IPSegmentEntity
from models.ip_management.functions import IPAddressesFunctions
from entities.ip_groups import IPGroupsEntity, IPGroupsTagsEntity
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, PrimaryKeyConstraint, text


class IPSegment(Base):
    __tablename__ = 'ip_segment'

    ip_segment_id = Column(Integer, primary_key=True, nullable=False)
    fk_router_id = Column(Integer, ForeignKey('routers.router_id'), nullable=False)
    ip_segment_ip = Column(String(15), nullable=False)
    ip_segment_mask = Column(String(15), nullable=False)
    ip_segment_network = Column(String(15), nullable=False)
    ip_segment_interface = Column(String(255), nullable=False)
    ip_segment_actual_iface = Column(String(255), nullable=False)
    ip_segment_tag = Column(Enum(IPSegmentTag), nullable=False)
    ip_segment_comment = Column(String(255), nullable=False)
    ip_segment_is_invalid = Column(Boolean, nullable=False)
    ip_segment_is_dynamic = Column(Boolean, nullable=False)
    ip_segment_is_disabled = Column(Boolean, nullable=False)

    def __repr__(self):
        return f'<IP Segment {self.ip_segment_id}>'

    def to_dict(self):
        return {
            'ip_segment_id': self.ip_segment_id,
            'fk_router_id': self.fk_router_id,
            'ip_segment_ip': self.ip_segment_ip,
            'ip_segment_mask': self.ip_segment_mask,
            'ip_segment_network': self.ip_segment_network,
            'ip_segment_interface': self.ip_segment_interface,
            'ip_segment_actual_iface': self.ip_segment_actual_iface,
            'ip_segment_tag': self.ip_segment_tag,
            'ip_segment_comment': self.ip_segment_comment,
            'ip_segment_is_invalid': self.ip_segment_is_invalid,
            'ip_segment_is_dynamic': self.ip_segment_is_dynamic,
            'ip_segment_is_disabled': self.ip_segment_is_disabled
        }

    @staticmethod
    def verify_autoincrement_id(session):
        try:
            if not session.query(IPSegment).all():
                session.execute(text("ALTER TABLE ip_segment AUTO_INCREMENT = 1"))
        except Exception as e:
            raise e

    @staticmethod
    def bulk_add_ip_segments(session, ip_segments: list[IPSegmentEntity]) -> None:
        """
        Add a list of IP segments to the database in bulk
        :arg session: The database session
        :arg ip_segments: The list of IP segments to possibly add to the database
        :return: None
        """

        try:
            # Create a list of IPSegment objects obtained from router
            bulk_list = [IPSegment(
                fk_router_id=ip_segment.fk_router_id,
                ip_segment_ip=ip_segment.ip_segment_ip,
                ip_segment_mask=ip_segment.ip_segment_mask,
                ip_segment_network=ip_segment.ip_segment_network,
                ip_segment_interface=ip_segment.ip_segment_interface,
                ip_segment_actual_iface=ip_segment.ip_segment_actual_iface,
                ip_segment_tag=ip_segment.ip_segment_tag,
                ip_segment_comment=ip_segment.ip_segment_comment,
                ip_segment_is_invalid=ip_segment.ip_segment_is_invalid,
                ip_segment_is_dynamic=ip_segment.ip_segment_is_dynamic,
                ip_segment_is_disabled=ip_segment.ip_segment_is_disabled
            ) for ip_segment in ip_segments]

            # Create a list of IPSegment objects to add to the database
            to_add = []

            # Iterate on the bulk list and check if the IP segment exists in the database
            for ip_segment in bulk_list:
                # Verify if the IP segment exists in the database, based on the IP address, mask and interface
                if (IPAddressesFunctions.validate_ip_segment_exists(
                        session,
                        ip_segment.ip_segment_ip,
                        ip_segment.ip_segment_mask,
                        ip_segment.ip_segment_interface
                )):
                    # If it does not exist, add it to the list
                    to_add.append(ip_segment)
                else:
                    # If it exists, update the IP segment in the database

                    # Get the IP segment from the database based on the IP address, mask and interface
                    ip_segment = session.query(IPSegment).filter(
                        IPSegment.ip_segment_ip == ip_segment.ip_segment_ip,
                        IPSegment.ip_segment_mask == ip_segment.ip_segment_mask,
                        IPSegment.ip_segment_interface == ip_segment.ip_segment_interface
                    ).first()

                    # Update the IP segment in the database
                    ip_segment.fk_router_id = ip_segment.fk_router_id
                    ip_segment.ip_segment_network = ip_segment.ip_segment_network
                    ip_segment.ip_segment_interface = ip_segment.ip_segment_interface
                    ip_segment.ip_segment_actual_iface = ip_segment.ip_segment_actual_iface
                    ip_segment.ip_segment_tag = ip_segment.ip_segment_tag
                    ip_segment.ip_segment_comment = ip_segment.ip_segment_comment
                    ip_segment.ip_segment_is_invalid = ip_segment.ip_segment_is_invalid
                    ip_segment.ip_segment_is_dynamic = ip_segment.ip_segment_is_dynamic
                    ip_segment.ip_segment_is_disabled = ip_segment.ip_segment_is_disabled

            # if there are IP segments to add, add them to the database in bulk
            if to_add:
                session.bulk_save_objects(to_add)
        except Exception as e:
            raise e

    @staticmethod
    def delete_ip_segment(session, ip_segment_id):
        try:
            from models.router_scan.models import ARP
            # from models.router_scan.models import ARPTags

            ip_groups = session.query(IPGroups).filter_by(fk_ip_segment_id=ip_segment_id).all()
            ip_group_ids = [ip_group.ip_group_id for ip_group in ip_groups]

            session.query(IPGroupsToIPGroupsTags).filter_by(fk_ip_group_id=ip_group_ids).delete(
                synchronize_session=False)
            session.query(IPGroups).filter(IPGroups.ip_group_id.in_(ip_group_ids)).delete(synchronize_session=False)

            arps = session.query(ARP.arp_id).filter_by(fk_ip_address_id=ip_segment_id).all()
            arp_ids = [arp.arp_id for arp in arps]

            if arp_ids:
                # session.query(ARPTags).filter(ARPTags.fk_arp_id.in_(arp_ids)).delete(synchronize_session=False)

                session.query(ARP).filter(ARP.arp_id.in_(arp_ids)).delete(synchronize_session=False)

            ip_segment = session.query(IPSegment).get(ip_segment_id)
            if ip_segment:
                session.delete(ip_segment)
        except Exception as e:
            raise e

    @staticmethod
    def delete_ip_segments(session):
        try:
            from models.router_scan.models import ARP
            # from models.router_scan.models import ARPTags

            session.query(IPGroupsToIPGroupsTags).delete()
            session.query(IPGroupsTags).delete()
            session.query(IPGroups).delete()

            # session.query(ARPTags).delete()
            session.query(ARP).delete()

            session.query(IPSegment).delete()
        except Exception as e:
            raise e

    @staticmethod
    def delete_ip_segments_by_site(session, site_id):
        try:
            from models.router_scan.models import ARP
            # from models.router_scan.models import ARPTags

            routers = session.query(Router).filter_by(fk_site_id=site_id).all()

            ip_segments = session.query(IPSegment).filter(
                IPSegment.fk_router_id.in_([router.router_id for router in routers])).all()
            ip_segment_ids = [ip_segment.ip_segment_id for ip_segment in ip_segments]

            ip_groups = session.query(IPGroups).filter(IPGroups.fk_ip_segment_id.in_(ip_segment_ids)).all()
            ip_group_ids = [ip_group.ip_group_id for ip_group in ip_groups]

            session.query(IPGroupsToIPGroupsTags).filter_by(
                IPGroupsToIPGroupsTags.fk_ip_group_id.in_(ip_group_ids)).delete(synchronize_session=False)
            session.query(IPGroups).filter(IPGroups.ip_group_id.in_(ip_group_ids)).delete(synchronize_session=False)

            arps = session.query(ARP.arp_id).filter(ARP.fk_ip_address_id.in_(ip_segment_ids)).all()
            arp_ids = [arp.arp_id for arp in arps]

            if arp_ids:
                # session.query(ARPTags).filter(ARPTags.fk_arp_id.in_(arp_ids)).delete(synchronize_session=False)
                session.query(ARP).filter(ARP.arp_id.in_(arp_ids)).delete(synchronize_session=False)

            session.query(IPSegment).filter(IPSegment.ip_segment_id.in_(ip_segment_ids)).delete(
                synchronize_session=False)
        except Exception as e:
            raise e

    @staticmethod
    def bulk_delete_ip_segments(session, segments_ids):
        try:
            from models.router_scan.models import ARP
            # from models.router_scan.models import ARPTags

            ip_groups = session.query(IPGroups).filter(IPGroups.fk_ip_segment_id.in_(segments_ids)).all()
            ip_group_ids = [ip_group.ip_group_id for ip_group in ip_groups]

            session.query(IPGroupsToIPGroupsTags).filter(
                IPGroupsToIPGroupsTags.fk_ip_group_id.in_(ip_group_ids)).delete(
                synchronize_session=False)
            session.query(IPGroups).filter(IPGroups.ip_group_id.in_(ip_group_ids)).delete(synchronize_session=False)

            arps = session.query(ARP.arp_id).filter(ARP.fk_ip_address_id.in_(segments_ids)).all()
            arp_ids = [arp.arp_id for arp in arps]

            if arp_ids:
                # session.query(ARPTags).filter(ARPTags.fk_arp_id.in_(arp_ids)).delete(synchronize_session=False)
                session.query(ARP).filter(ARP.arp_id.in_(arp_ids)).delete(synchronize_session=False)

            session.query(IPSegment).filter(IPSegment.ip_segment_id.in_(segments_ids)).delete(synchronize_session=False)
        except Exception as e:
            raise e

    @staticmethod
    def get_ip_segment(session, ip_segment_id):
        try:
            ip_segment = session.query(IPSegment).get(ip_segment_id)
            obj = IPSegmentEntity(
                ip_segment_id=ip_segment.ip_segment_id,
                fk_router_id=ip_segment.fk_router_id,
                ip_segment_ip=ip_segment.ip_segment_ip,
                ip_segment_mask=ip_segment.ip_segment_mask,
                ip_segment_network=ip_segment.ip_segment_network,
                ip_segment_interface=ip_segment.ip_segment_interface,
                ip_segment_actual_iface=ip_segment.ip_segment_actual_iface,
                ip_segment_tag=ip_segment.ip_segment_tag,
                ip_segment_comment=ip_segment.ip_segment_comment,
                ip_segment_is_invalid=ip_segment.ip_segment_is_invalid,
                ip_segment_is_dynamic=ip_segment.ip_segment_is_dynamic,
                ip_segment_is_disabled=ip_segment.ip_segment_is_disabled
            )
            return obj
        except Exception as e:
            raise e

    @staticmethod
    def get_ip_segments(session):
        try:
            ip_segments = session.query(IPSegment).all()
            ip_segment_list = []
            for ip_segment in ip_segments:
                obj = IPSegmentEntity(
                    ip_segment_id=ip_segment.ip_segment_id,
                    fk_router_id=ip_segment.fk_router_id,
                    ip_segment_ip=ip_segment.ip_segment_ip,
                    ip_segment_mask=ip_segment.ip_segment_mask,
                    ip_segment_network=ip_segment.ip_segment_network,
                    ip_segment_interface=ip_segment.ip_segment_interface,
                    ip_segment_actual_iface=ip_segment.ip_segment_actual_iface,
                    ip_segment_tag=ip_segment.ip_segment_tag,
                    ip_segment_comment=ip_segment.ip_segment_comment,
                    ip_segment_is_invalid=ip_segment.ip_segment_is_invalid,
                    ip_segment_is_dynamic=ip_segment.ip_segment_is_dynamic,
                    ip_segment_is_disabled=ip_segment.ip_segment_is_disabled
                )
                ip_segment_list.append(obj)
            return ip_segment_list
        except Exception as e:
            raise e

    @staticmethod
    def get_ip_segments_by_site_id(session, site_id: str):
        try:
            router = session.query(Router).filter_by(fk_site_id=site_id).first()
            ip_segments = session.query(IPSegment).filter_by(fk_router_id=router.router_id).all()
            ip_segment_list = []
            for ip_segment in ip_segments:
                obj = IPSegmentEntity(
                    ip_segment_id=ip_segment.ip_segment_id,
                    fk_router_id=ip_segment.fk_router_id,
                    ip_segment_ip=ip_segment.ip_segment_ip,
                    ip_segment_mask=ip_segment.ip_segment_mask,
                    ip_segment_network=ip_segment.ip_segment_network,
                    ip_segment_interface=ip_segment.ip_segment_interface,
                    ip_segment_actual_iface=ip_segment.ip_segment_actual_iface,
                    ip_segment_tag=ip_segment.ip_segment_tag,
                    ip_segment_comment=ip_segment.ip_segment_comment,
                    ip_segment_is_invalid=ip_segment.ip_segment_is_invalid,
                    ip_segment_is_dynamic=ip_segment.ip_segment_is_dynamic,
                    ip_segment_is_disabled=ip_segment.ip_segment_is_disabled
                )
                ip_segment_list.append(obj)
            return ip_segment_list
        except Exception as e:
            raise e

    @staticmethod
    def get_ip_segments_by_router_id(session, router_id: int) -> list[IPSegmentEntity]:
        """
        Get IP segments by router ID
        :param session: The database session
        :param router_id: The router ID
        :return: List of IP segments
        """
        try:
            # List of IP segments
            ip_segment_list = []

            # Obtain all IP segments from the database based on the router ID
            ip_segments = session.query(IPSegment).filter_by(fk_router_id=router_id).all()

            # Iterate on the IP segments and create a list of IP segments
            for ip_segment in ip_segments:
                # Create the IP segment object
                obj = IPSegmentEntity(
                    ip_segment_id=ip_segment.ip_segment_id,
                    fk_router_id=ip_segment.fk_router_id,
                    ip_segment_ip=ip_segment.ip_segment_ip,
                    ip_segment_mask=ip_segment.ip_segment_mask,
                    ip_segment_network=ip_segment.ip_segment_network,
                    ip_segment_interface=ip_segment.ip_segment_interface,
                    ip_segment_actual_iface=ip_segment.ip_segment_actual_iface,
                    ip_segment_tag=ip_segment.ip_segment_tag,
                    ip_segment_comment=ip_segment.ip_segment_comment,
                    ip_segment_is_invalid=ip_segment.ip_segment_is_invalid,
                    ip_segment_is_dynamic=ip_segment.ip_segment_is_dynamic,
                    ip_segment_is_disabled=ip_segment.ip_segment_is_disabled
                )
                # Append the IP segment object to the list
                ip_segment_list.append(obj)
            return ip_segment_list
        except Exception as e:
            raise e


class IPGroupsTags(Base):
    __tablename__ = 'ip_groups_tags'

    ip_group_tag_id = Column(Integer, primary_key=True, nullable=False)
    ip_group_tag_name = Column(String(255), nullable=False)
    ip_group_tag_color = Column(String(7), nullable=False, default='#30f2f2')
    ip_group_tag_text_color = Column(String(7), nullable=False, default='#FFFFFF')
    ip_group_tag_description = Column(String(255), nullable=True, default='')

    def __repr__(self):
        return f'<IP Group Tag {self.ip_group_tag_id}>'

    """
    def __dict__(self):
        return {
            'ip_group_tag_id': self.ip_group_tag_id,
            'ip_group_tag_name': self.ip_group_tag_name,
            'ip_group_tag_color': self.ip_group_tag_color,
            'ip_group_tag_text_color': self.ip_group_tag_text_color,
            'ip_group_tag_description': self.ip_group_tag_description
        }
    """

    @staticmethod
    def verify_autoincrement_id(session):
        try:
            if not session.query(IPGroupsTags).all():
                session.execute(text("ALTER TABLE ip_groups_tags AUTO_INCREMENT = 1"))
        except Exception as e:
            raise e

    @staticmethod
    def add_ip_group_tag(session, ip_group_tag: IPGroupsTagsEntity):
        """
        Add an IP group tag to the database
        :param session: The database session
        :param ip_group_tag: The IP group tag to add to the database
        :return: None
        """
        try:
            # Create the IP group tag object

            ip_group_tag_obj = IPGroupsTags(
                ip_group_tag_name=ip_group_tag.ip_group_tag_name,
                ip_group_tag_color=ip_group_tag.ip_group_tag_color,
                ip_group_tag_text_color=ip_group_tag.ip_group_tag_text_color,
                ip_group_tag_description=ip_group_tag.ip_group_tag_description
            )

            # Add the IP group tag to the database
            session.add(ip_group_tag_obj)
        except Exception as e:
            raise e

    @staticmethod
    def update_ip_group_tag(session, ip_group_tag: IPGroupsTagsEntity):
        """
        Update an IP group tag in the database
        :param session: The database session
        :param ip_group_tag: The IP group tag to update in the database
        :return: None
        """
        try:
            # Get the IP group tag from the database based on the IP group tag ID
            ip_group_tag_obj = session.query(IPGroupsTags).get(ip_group_tag.ip_group_tag_id)

            # Update the IP group tag in the database
            ip_group_tag_obj.ip_group_tag_name = ip_group_tag.ip_group_tag_name
            ip_group_tag_obj.ip_group_tag_color = ip_group_tag.ip_group_tag_color
            ip_group_tag_obj.ip_group_tag_text_color = ip_group_tag.ip_group_tag_text_color
            ip_group_tag_obj.ip_group_tag_description = ip_group_tag.ip_group_tag_description
        except Exception as e:
            raise e

    @staticmethod
    def delete_ip_group_tag(session, ip_group_tag_id):
        """
        Delete an IP group tag from the database
        :param session: The database session
        :param ip_group_tag_id: The IP group tag ID
        :return: None
        """
        try:
            # Get the IP group tag from the database based on the IP group tag ID
            ip_group_tag_obj = session.query(IPGroupsTags).get(ip_group_tag_id)

            # Delete the IP group tag from the database
            session.query(IPGroupsToIPGroupsTags).filter_by(fk_ip_group_tag_id=ip_group_tag_id).delete(
                synchronize_session=False)
            session.delete(ip_group_tag_obj)
        except Exception as e:
            raise e

    @staticmethod
    def bulk_delete_ip_group_tags(session, ip_group_tag_ids: list):
        """
        Delete a list of IP group tags from the database
        :param session: The database session
        :param ip_group_tag_ids: The list of IP group tag IDs to delete
        :return: None
        """
        try:
            # Delete all IP group tags from the database based on the list of IP group tag IDs
            session.query(IPGroupsToIPGroupsTags).filter(
                IPGroupsToIPGroupsTags.fk_ip_group_tag_id.in_(ip_group_tag_ids)).delete(synchronize_session=False)
            session.query(IPGroupsTags).filter(IPGroupsTags.ip_group_tag_id.in_(ip_group_tag_ids)).delete(
                synchronize_session=False)
        except Exception as e:
            raise e

    @staticmethod
    def delete_ip_group_tags(session):
        """
        Delete all IP group tags from the database
        :param session: The database session
        :return: None
        """
        try:
            # Get all IP group tags from the database
            ip_group_tags = session.query(IPGroupsTags).all()

            # Make a list of ids to delete
            ip_group_tag_ids = [ip_group_tag.ip_group_tag_id for ip_group_tag in ip_group_tags]

            # Delete all IP group tags from the database
            session.query(IPGroupsToIPGroupsTags).filter(
                IPGroupsToIPGroupsTags.fk_ip_group_tag_id.in_(ip_group_tag_ids)).delete(synchronize_session=False)
            session.query(IPGroupsTags).filter(IPGroupsTags.ip_group_tag_id.in_(ip_group_tag_ids)).delete(
                synchronize_session=False)
        except Exception as e:
            raise e

    @staticmethod
    def get_ip_group_tag(session, ip_group_tag_id):
        """
        Get an IP group tag from the database
        :param session: The database session
        :param ip_group_tag_id: The IP group tag ID
        :return: The IP group tag object
        """
        try:
            # Get the IP group tag from the database based on the IP group tag ID
            ip_group_tag_obj = session.query(IPGroupsTags).get(ip_group_tag_id)
            return IPGroupsTagsEntity(
                ip_group_tag_id=ip_group_tag_obj.ip_group_tag_id,
                ip_group_tag_name=ip_group_tag_obj.ip_group_tag_name,
                ip_group_tag_color=ip_group_tag_obj.ip_group_tag_color,
                ip_group_tag_text_color=ip_group_tag_obj.ip_group_tag_text_color,
                ip_group_tag_description=ip_group_tag_obj.ip_group_tag_description
            )
        except Exception as e:
            raise e

    @staticmethod
    def get_ip_group_tags(session):
        """
        Get all IP group tags from the database
        :param session: The database session
        :return: List of IP group tags
        """
        try:
            # Get all IP group tags from the database
            ip_group_tags = session.query(IPGroupsTags).all()
            ip_group_tags_list = []
            for ip_group_tag in ip_group_tags:
                ip_group_tags_list.append(IPGroupsTagsEntity(
                    ip_group_tag_id=ip_group_tag.ip_group_tag_id,
                    ip_group_tag_name=ip_group_tag.ip_group_tag_name,
                    ip_group_tag_color=ip_group_tag.ip_group_tag_color,
                    ip_group_tag_text_color=ip_group_tag.ip_group_tag_text_color,
                    ip_group_tag_description=ip_group_tag.ip_group_tag_description
                ))
            return ip_group_tags_list
        except Exception as e:
            raise e

    @staticmethod
    def get_tags_by_ip_group_id(session, ip_group_id: int) -> list[IPGroupsTagsEntity]:
        """
        Get tags by IP group ID
        :param session: The database session
        :param ip_group_id: The IP group ID
        :return: List of IP group tags
        """
        try:
            # Get all IP group to IP group tag objects from the database based on the IP group ID
            ip_group_to_tags = session.query(IPGroupsToIPGroupsTags).filter_by(fk_ip_group_id=ip_group_id).all()
            ip_group_tags_list = []
            for ip_group_to_tag in ip_group_to_tags:
                # Get the IP group tag object from the database based on the IP group tag ID
                ip_group_tag = session.query(IPGroupsTags).get(ip_group_to_tag.fk_ip_group_tag_id)
                ip_group_tags_list.append(IPGroupsTagsEntity(
                    ip_group_tag_id=ip_group_tag.ip_group_tag_id,
                    ip_group_tag_name=ip_group_tag.ip_group_tag_name,
                    ip_group_tag_color=ip_group_tag.ip_group_tag_color,
                    ip_group_tag_text_color=ip_group_tag.ip_group_tag_text_color,
                    ip_group_tag_description=ip_group_tag.ip_group_tag_description
                ))
            return ip_group_tags_list
        except Exception as e:
            raise e


class IPGroupsToIPGroupsTags(Base):
    __tablename__ = 'ip_groups_to_ip_groups_tags'

    fk_ip_group_id = Column(Integer, ForeignKey('ip_groups.ip_group_id'), nullable=False)
    fk_ip_group_tag_id = Column(Integer, ForeignKey('ip_groups_tags.ip_group_tag_id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('fk_ip_group_id', 'fk_ip_group_tag_id'),
    )

    def __repr__(self):
        return f'<IP Group to IP Group Tag {self.fk_ip_group_id} <-> {self.fk_ip_group_tag_id}>'

    @staticmethod
    def verify_autoincrement_id(session):
        try:
            if not session.query(IPGroupsToIPGroupsTags).all():
                session.execute(text("ALTER TABLE ip_groups_to_ip_groups_tags AUTO_INCREMENT = 1"))
        except Exception as e:
            raise e

    @staticmethod
    def assign_tag(session, tag_metadata: dict) -> None:
        """
        Assign a tag to an IP group
        :param session: The database session
        :param ip_group_id: The IP group ID
        :param ip_group_tag_id: The IP group tag ID
        :return: None
        """
        try:
            # Check if the tag is already assigned to the IP group
            ip_group_to_tag = session.query(IPGroupsToIPGroupsTags).filter_by(
                fk_ip_group_id=tag_metadata['ip_group_id'],
                fk_ip_group_tag_id=tag_metadata['ip_group_tag_id']
            ).first()

            # If the tag is not assigned to the IP group, assign it
            if not ip_group_to_tag:
                # Create the IP group to IP group tag object
                ip_group = IPGroupsToIPGroupsTags(
                    fk_ip_group_id=tag_metadata['ip_group_id'],
                    fk_ip_group_tag_id=tag_metadata['ip_group_tag_id']
                )

                # Add the IP group to IP group tag object to the database
                session.add(ip_group)
            # If the tag is already assigned to the IP group, update it
            else:
                # Do nothing
                pass
        except Exception as e:
            raise e

    @staticmethod
    def unassign_tag(session, tag_metadata: dict) -> None:
        """
        Unassign a tag from an IP group
        :param session: The database session
        :param ip_group_id: The IP group ID
        :param ip_group_tag_id: The IP group tag ID
        :return: None
        """
        try:
            # Get the IP group to IP group tag object from the database based on the IP group ID and IP group tag ID
            ip_group_to_tag = session.query(IPGroupsToIPGroupsTags).filter_by(
                fk_ip_group_id=tag_metadata['ip_group_id'],
                fk_ip_group_tag_id=tag_metadata['ip_group_tag_id']
            ).first()

            # Delete the IP group to IP group tag object from the database
            session.delete(ip_group_to_tag)
        except Exception as e:
            raise e

    @staticmethod
    def unassing_all_tags(session, ip_group_id: int) -> None:
        """
        Unassign all tags from an IP group
        :param session: The database session
        :param ip_group_id: The IP group ID
        :return: None
        """
        try:
            # Get all IP group to IP group tag objects from the database based on the IP group ID
            ip_group_to_tags = session.query(IPGroupsToIPGroupsTags).filter_by(fk_ip_group_id=ip_group_id).all()

            # Delete all IP group to IP group tag objects from the database based on the IP group ID
            for ip_group_to_tag in ip_group_to_tags:
                session.delete(ip_group_to_tag)
        except Exception as e:
            raise e

    @staticmethod
    def get_tags_by_ip_group_id(session, ip_group_id: int) -> list[IPGroupsTagsEntity]:
        """
        Get tags by IP group ID
        :param session: The database session
        :param ip_group_id: The IP group ID
        :return: List of IP group tags
        """
        try:
            # Get all IP group to IP group tag objects from the database based on the IP group ID
            ip_group_to_tags = session.query(IPGroupsToIPGroupsTags).filter_by(fk_ip_group_id=ip_group_id).all()
            ip_group_tags_list = []
            for ip_group_to_tag in ip_group_to_tags:
                # Get the IP group tag object from the database based on the IP group tag ID
                ip_group_tag = session.query(IPGroupsTags).get(ip_group_to_tag.fk_ip_group_tag_id)
                ip_group_tags_list.append(IPGroupsTagsEntity(
                    ip_group_tag_id=ip_group_tag.ip_group_tag_id,
                    ip_group_tag_name=ip_group_tag.ip_group_tag_name,
                    ip_group_tag_color=ip_group_tag.ip_group_tag_color,
                    ip_group_tag_text_color=ip_group_tag.ip_group_tag_text_color,
                    ip_group_tag_description=ip_group_tag.ip_group_tag_description
                ))
            return ip_group_tags_list
        except Exception as e:
            raise e

    @staticmethod
    def get_tags_ids_by_ip_group_id(session, ip_group_id: int) -> list[int]:
        """
        Get tags IDs by IP group ID
        :param session: The database session
        :param ip_group_id: The IP group ID
        :return: List of IP group tags IDs
        """
        try:
            # Get all IP group to IP group tag objects from the database based on the IP group ID
            ip_group_to_tags = session.query(IPGroupsToIPGroupsTags).filter_by(fk_ip_group_id=ip_group_id).all()
            ip_group_tags_list = []
            for ip_group_to_tag in ip_group_to_tags:
                ip_group_tags_list.append(ip_group_to_tag.fk_ip_group_tag_id)
            return ip_group_tags_list
        except Exception as e:
            raise e


class IPGroups(Base):
    __tablename__ = 'ip_groups'

    types_values = ['public', 'private']
    status_values = ['blacklist', 'authorized', 'unknown']

    ip_group_id = Column(Integer, primary_key=True, nullable=False)
    fk_ip_segment_id = Column(Integer, ForeignKey('ip_segment.ip_segment_id'), nullable=False)
    ip_group_name = Column(Enum(*status_values, name="status_enum"), nullable=False)
    ip_group_type = Column(Enum(*types_values, name="types_enum"), nullable=False)
    ip_group_alias = Column(String(255), nullable=True)
    ip_group_description = Column(String(255), nullable=True)
    ip_group_ip = Column(String(15), nullable=False)
    ip_group_mask = Column(String(15), nullable=False)
    ip_group_mac = Column(String(17), nullable=True)
    ip_group_mac_vendor = Column(String(255), nullable=True)
    ip_group_interface = Column(String(255), nullable=False)
    ip_group_comment = Column(String(255), nullable=True)
    ip_is_dhcp = Column(Boolean, nullable=False)
    ip_is_dynamic = Column(Boolean, nullable=False)
    ip_is_complete = Column(Boolean, nullable=False)
    ip_is_disabled = Column(Boolean, nullable=False)
    ip_is_published = Column(Boolean, nullable=False)
    ip_duplicity = Column(Boolean, nullable=False, default=False)
    ip_duplicity_indexes = Column(String(511), nullable=True, default='')

    ip_groups = relationship('IPSegment', backref=backref('ip_groups', lazy=True))

    def __repr__(self):
        return f'<IP Group {self.ip_group_id}>'

    """
    def __dict__(self):
        return {
            'ip_group_id': self.ip_group_id,
            'fk_ip_segment_id': self.fk_ip_segment_id,
            'ip_group_name': self.ip_group_name,
            'ip_group_type': self.ip_group_type,
            'ip_group_alias': self.ip_group_alias,
            'ip_group_description': self.ip_group_description,
            'ip_group_ip': self.ip_group_ip,
            'ip_group_mask': self.ip_group_mask,
            'ip_group_mac': self.ip_group_mac,
            'ip_group_mac_vendor': self.ip_group_mac_vendor,
            'ip_group_interface': self.ip_group_interface,
            'ip_group_comment': self.ip_group_comment,
            'ip_is_dhcp': self.ip_is_dhcp,
            'ip_is_dynamic': self.ip_is_dynamic,
            'ip_is_complete': self.ip_is_complete,
            'ip_is_disabled': self.ip_is_disabled,
            'ip_is_published': self.ip_is_published,
            'ip_duplicity': self.ip_duplicity,
            'ip_duplicity_indexes': self.ip_duplicity_indexes
        }
    """

    @staticmethod
    def verify_autoincrement_id(session):
        try:
            if not session.query(IPGroups).all():
                session.execute(text("ALTER TABLE ip_groups AUTO_INCREMENT = 1"))
        except Exception as e:
            raise e

    @staticmethod
    def bulk_add_ip_groups(session, ip_group_list: list) -> None:
        """
        Add a list of IP groups to the database in bulk
        :param session: The database session
        :param ip_group_list: The list of IP groups to add to the database
        :return: None
        """
        try:
            session.bulk_save_objects(ip_group_list)
        except Exception as e:
            raise e

    @staticmethod
    def bulk_update_ip_groups(session, ip_group_list: list) -> None:
        """
        Update a list of IP groups in the database in bulk
        :param session: The database session
        :param ip_group_list: The list of IP groups to update in the database
        :return: None
        """
        try:
            # Iterate on the list of IP groups
            for ip_group in ip_group_list:
                # Get the IP group from the database based on the IP group ID
                ip_group_x = session.query(IPGroups).filter_by(
                    ip_group_ip=ip_group.ip_group_ip,
                    ip_group_interface=ip_group.ip_group_interface
                ).first()

                # Update the IP group in the database
                ip_group_x.ip_group_name = ip_group.ip_group_name
                ip_group_x.ip_group_type = ip_group.ip_group_type
                ip_group_x.ip_group_ip = ip_group.ip_group_ip
                ip_group_x.ip_group_mask = ip_group.ip_group_mask
                ip_group_x.ip_group_mac = ip_group.ip_group_mac
                ip_group_x.ip_group_mac_vendor = ip_group.ip_group_mac_vendor
                ip_group_x.ip_group_interface = ip_group.ip_group_interface
                ip_group_x.ip_group_comment = ip_group.ip_group_comment
                ip_group_x.ip_is_dhcp = ip_group.ip_is_dhcp
                ip_group_x.ip_is_dynamic = ip_group.ip_is_dynamic
                ip_group_x.ip_is_complete = ip_group.ip_is_complete
                ip_group_x.ip_is_disabled = ip_group.ip_is_disabled
                ip_group_x.ip_is_published = ip_group.ip_is_published
                ip_group_x.ip_duplicity = ip_group.ip_duplicity
                ip_group_x.ip_duplicity_indexes = ip_group.ip_duplicity_indexes
        except Exception as e:
            raise e

    @staticmethod
    def update_ip_group(session, ip_group_metadata: dict) -> None:
        """
        Update an IP group in the database
        :param session: Database session
        :param ip_group_metadata: The IP group metadata
        :return: None
        """
        try:
            # Import the necessary modules
            from utils.threading_manager import ThreadingManager

            # Get the IP group from the database based on the IP group ID
            ip_group_x = session.query(IPGroups).get(ip_group_metadata['ip_group'].ip_group_id)
            old_tags = ThreadingManager().run_thread(IPGroupsToIPGroupsTags.get_tags_ids_by_ip_group_id, 'rx',
                                                     ip_group_metadata['ip_group'].ip_group_id)

            print(f"old_tags: {old_tags}")

            # Update the IP group in the database
            ip_group_x.ip_group_alias = ip_group_metadata['ip_group'].ip_group_alias
            ip_group_x.ip_group_description = ip_group_metadata['ip_group'].ip_group_description

            session.commit()

            # Verify if there are tags to assign and unassign
            if ip_group_metadata['tags'][0] != -1:
                # Check what tags to assign and unassign
                tags_to_assign = set(ip_group_metadata['tags'])
                tags_to_unassign = set(set(old_tags) - tags_to_assign)

                print(f"tags_to_assign: {tags_to_assign}")
                print(f"tags_to_unassign: {tags_to_unassign}")

                if tags_to_unassign or tags_to_assign:
                    # Verify if there are tags to assign
                    if tags_to_assign:
                        # Iterate in the tags to assign to the IP group
                        for tag in tags_to_assign:
                            # Assign the tag to the IP group
                            tag_metadata = {
                                'ip_group_id': ip_group_metadata['ip_group'].ip_group_id,
                                'ip_group_tag_id': tag
                            }
                            ThreadingManager().run_thread(IPGroupsToIPGroupsTags.assign_tag, 'w', tag_metadata)

                    # Verify if there are tags to unassign
                    if tags_to_unassign:
                        # Iterate in the tags to unassign from the IP group
                        for tag in tags_to_unassign:
                            tag_metadata = {
                                'ip_group_id': ip_group_metadata['ip_group'].ip_group_id,
                                'ip_group_tag_id': tag
                            }
                            # Unassign the tag from the IP group
                            ThreadingManager().run_thread(IPGroupsToIPGroupsTags.unassign_tag, 'w', tag_metadata)
                        ThreadingManager().run_thread(IPGroupsToIPGroupsTags.verify_autoincrement_id, 'r')
            else:
                # Unassign all tags from the IP group
                ThreadingManager().run_thread(IPGroupsToIPGroupsTags.unassing_all_tags, 'w',
                                              ip_group_metadata['ip_group'].ip_group_id)
                ThreadingManager().run_thread(IPGroupsToIPGroupsTags.verify_autoincrement_id, 'r')
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def bulk_move_ip_groups_to_arp(session, ip_group_ids: list) -> None:
        """
        Move a list of IP groups to ARP
        :param session: The database session
        :param ip_group_ids: The list of IP group IDs to move to ARP
        :return: None
        """
        try:
            # Import the ARP model
            from models.router_scan.models import ARP

            # Get all IP groups from the database based on the IP group IDs
            ip_groups = session.query(IPGroups).filter(IPGroups.ip_group_id.in_(ip_group_ids)).all()

            # Create a list of ARP objects to add to the database
            arps = []
            for ip_group in ip_groups:
                arps.append(ARP(
                    fk_ip_address_id=ip_group.fk_ip_segment_id,
                    arp_ip=ip_group.ip_group_ip,
                    arp_mac=ip_group.ip_group_mac,
                    arp_alias=ip_group.ip_group_alias,
                    arp_tag=ip_group.ip_group_type,
                    arp_interface=ip_group.ip_group_interface,
                    arp_is_dhcp=ip_group.ip_is_dhcp,
                    arp_is_invalid=ip_group.ip_is_invalid,
                    arp_is_dynamic=ip_group.ip_is_dynamic,
                    arp_is_disabled=ip_group.ip_is_disabled,
                    arp_is_published=ip_group.ip_is_published,
                    arp_duplicity=False,
                    arp_duplicity_indexes=''
                ))

            # Delete the IP groups from the database
            session.query(IPGroups).filter(IPGroups.ip_group_id.in_(ip_group_ids)).delete(synchronize_session=False)

            # Add the ARP objects to the database
            session.bulk_save_objects(arps)
        except Exception as e:
            raise e

    @staticmethod
    def move_from_blacklist_to_authorized(session, ip_group_id: int) -> None:
        """
        Move an IP group from blacklist to authorized
        :param session: The database session
        :param ip_group_id: The IP group ID
        :return: None
        """
        try:
            # Get the IP group from the database based on the IP group ID
            ip_group = session.query(IPGroups).get(ip_group_id)

            # Update the IP group in the database
            ip_group.ip_group_name = 'authorized'
        except Exception as e:
            raise e

    @staticmethod
    def bulk_move_from_blacklist_to_authorized(session, ip_group_ids: list[int]) -> None:
        """
        Move a list of IP groups from blacklist to authorized
        :param session: The database session
        :param ip_group_ids: The list of IP group IDs
        :return: None
        """
        try:
            # Get all IP groups from the database based on the IP group IDs
            ip_groups = session.query(IPGroups).filter(IPGroups.ip_group_id.in_(ip_group_ids)).all()

            # Iterate on the IP groups and update them in the database
            for ip_group in ip_groups:
                ip_group.ip_group_name = 'authorized'
        except Exception as e:
            raise e

    @staticmethod
    def move_all_from_blacklist_to_authorized(session, group_metadata: dict) -> None:
        """
        Move all IP groups from blacklist to authorized
        :param session: The database session
        :param group_metadata: The group metadata
        :return: None
        """
        try:
            # Get router from the database based on the site ID
            router = session.query(Router).filter_by(fk_site_id=group_metadata['site_id']).first()

            # Get all IP groups from the database based on the router ID
            ip_segments = session.query(IPSegment).filter_by(fk_router_id=router.router_id).all()

            # Make a list of IP segment IDs
            ip_segment_ids = [ip_segment.ip_segment_id for ip_segment in ip_segments]

            # Get all IP groups from the database based on the IP segment IDs
            ip_groups = session.query(IPGroups).filter(
                IPGroups.fk_ip_segment_id.in_(ip_segment_ids), IPGroups.ip_group_name == group_metadata['group']
            ).all()

            # Iterate on the IP groups and update them in the database
            for ip_group in ip_groups:
                ip_group.ip_group_name = 'authorized'
        except Exception as e:
            raise e

    @staticmethod
    def delete_ip_group(session, ip_group_id: int) -> None:
        """
        Delete an IP group from the database
        :param session: The database session
        :param ip_group_id: The IP group ID
        :return: None
        """
        try:
            # Get the tags assigned to the IP group
            tags = session.query(IPGroupsToIPGroupsTags).filter_by(fk_ip_group_id=ip_group_id).all()
            tags_ids = [tag.fk_ip_group_tag_id for tag in tags]

            # Get the IP group from the database based on the IP group ID
            ip_group = session.query(IPGroups).get(ip_group_id)

            # Delete the tags assigned to the IP group and the IP group from the database
            session.query(IPGroupsToIPGroupsTags).filter(IPGroupsToIPGroupsTags.fk_ip_group_id.in_(tags_ids)).delete(
                synchronize_session=False)
            session.delete(ip_group)
        except Exception as e:
            raise e

    @staticmethod
    def bulk_delete_ip_groups(session, ip_group_list: list) -> None:
        """
        Delete a list of IP groups from the database
        :param session: The database session
        :param ip_group_list: The list of IP groups to delete
        :return: None
        """

        try:
            # Delete the tags assigned to the IP groups and the IP groups from the database
            session.query(IPGroupsToIPGroupsTags).filter(IPGroupsToIPGroupsTags.fk_ip_group_id.in_(
                [ip_group.ip_group_id for ip_group in ip_group_list])).delete(synchronize_session=False)
            session.query(IPGroups).filter(IPGroups.ip_group_id.in_([ip_group.ip_group_id for ip_group in ip_group_list])).delete(
                synchronize_session=False)
        except Exception as e:
            raise e

    @staticmethod
    def delete_ip_groups(session) -> None:
        """
        Delete all IP groups from the database
        :param session: The database session
        :return: None
        """
        try:
            # Get all IP groups and their tags from the database
            ip_groups = session.query(IPGroups).all()

            # Make a list of ids to delete
            ip_group_ids = [ip_group.ip_group_id for ip_group in ip_groups]

            # Delete all IP groups from the database
            session.query(IPGroupsToIPGroupsTags).filter(
                IPGroupsToIPGroupsTags.fk_ip_group_id.in_(ip_group_ids)).delete(synchronize_session=False)
            session.query(IPGroups).filter(IPGroups.ip_group_id.in_(ip_group_ids)).delete(synchronize_session=False)
        except Exception as e:
            raise e

    @staticmethod
    def delete_ip_group_by_site(session, group_metadata: dict) -> list:
        try:
            router = session.query(Router).filter_by(fk_site_id=group_metadata['site_id']).first()
            segments = session.query(IPSegment).filter_by(fk_router_id=router.router_id).all()

            segments_ids = [segment.ip_segment_id for segment in segments]

            ip_groups = session.query(IPGroups).filter(
                IPGroups.ip_group_name == group_metadata['group'],
                IPGroups.fk_ip_segment_id.in_(segments_ids)
            ).all()
            ip_group_ids = [ip_group.ip_group_id for ip_group in ip_groups]

            session.query(IPGroupsToIPGroupsTags).filter(
                IPGroupsToIPGroupsTags.fk_ip_group_id.in_(ip_group_ids)).delete(
                synchronize_session=False)
            session.query(IPGroups).filter(IPGroups.ip_group_id.in_(ip_group_ids)).delete(synchronize_session=False)
        except Exception as e:
            raise e

    @staticmethod
    def get_ip_group(session, ip_group_id: int) -> list:
        """
        Get an IP group from the database
        :param session: The database session
        :param ip_group_id: The IP group ID
        :return: The IP group object
        """
        try:
            # List of IP groups and their tags
            ip_group_tags_list = []

            # Get the IP group from the database based on the IP group ID
            ip_group = session.query(IPGroups).get(ip_group_id)

            # Append the IP group object to the list
            ip_group_tags_list.append(
                IPGroupsEntity(
                    ip_group_id=ip_group.ip_group_id,
                    fk_ip_segment_id=ip_group.fk_ip_segment_id,
                    ip_group_name=ip_group.ip_group_name,
                    ip_group_type=ip_group.ip_group_type,
                    ip_group_alias=ip_group.ip_group_alias,
                    ip_group_description=ip_group.ip_group_description,
                    ip_group_ip=ip_group.ip_group_ip,
                    ip_group_mask=ip_group.ip_group_mask,
                    ip_group_mac=ip_group.ip_group_mac,
                    ip_group_mac_vendor=ip_group.ip_group_mac_vendor,
                    ip_group_interface=ip_group.ip_group_interface,
                    ip_group_comment=ip_group.ip_group_comment,
                    ip_is_dhcp=ip_group.ip_is_dhcp,
                    ip_is_dynamic=ip_group.ip_is_dynamic,
                    ip_is_complete=ip_group.ip_is_complete,
                    ip_is_disabled=ip_group.ip_is_disabled,
                    ip_is_published=ip_group.ip_is_published,
                    ip_duplicity=ip_group.ip_duplicity,
                    ip_duplicity_indexes=ip_group.ip_duplicity_indexes
                )
            )

            # Get the tags assigned to the IP group
            tags = session.query(IPGroupsToIPGroupsTags).filter_by(fk_ip_group_id=ip_group_id).all()

            # Iterate on the tags and create a list of IP group tags
            tag_list = []
            for tag in tags:
                # Get the IP group tag object from the database based on the IP group tag ID
                ip_group_tag = session.query(IPGroupsTags).get(tag.fk_ip_group_tag_id)
                tag_list.append(
                    IPGroupsTagsEntity(
                        ip_group_tag_id=ip_group_tag.ip_group_tag_id,
                        ip_group_tag_name=ip_group_tag.ip_group_tag_name,
                        ip_group_tag_color=ip_group_tag.ip_group_tag_color,
                        ip_group_tag_text_color=ip_group_tag.ip_group_tag_text_color,
                        ip_group_tag_description=ip_group_tag.ip_group_tag_description
                    )
                )

            # Append the IP group tags to the list
            ip_group_tags_list.append(tag_list)

            # Return the list of IP groups and their tags
            return ip_group_tags_list
        except Exception as e:
            raise e

    @staticmethod
    def get_ip_groups(session) -> list[tuple]:
        """
        Get all IP groups from the database
        :param session: The database session
        :return: List of IP groups
        """
        try:
            # List of IP groups and their tags
            ip_group_tags_list = []

            # Get all IP groups from the database
            ip_groups = session.query(IPGroups).all()

            # Get all associated tags for each IP group
            tags = session.query(IPGroupsToIPGroupsTags).all()

            for ip_group in ip_groups:
                # Create an object for the IP group
                ip_group_obj = IPGroupsEntity(
                    ip_group_id=ip_group.ip_group_id,
                    fk_ip_segment_id=ip_group.fk_ip_segment_id,
                    ip_group_name=ip_group.ip_group_name,
                    ip_group_type=ip_group.ip_group_type,
                    ip_group_alias=ip_group.ip_group_alias,
                    ip_group_description=ip_group.ip_group_description,
                    ip_group_ip=ip_group.ip_group_ip,
                    ip_group_mask=ip_group.ip_group_mask,
                    ip_group_mac=ip_group.ip_group_mac,
                    ip_group_mac_vendor=ip_group.ip_group_mac_vendor,
                    ip_group_interface=ip_group.ip_group_interface,
                    ip_group_comment=ip_group.ip_group_comment,
                    ip_is_dhcp=ip_group.ip_is_dhcp,
                    ip_is_dynamic=ip_group.ip_is_dynamic,
                    ip_is_complete=ip_group.ip_is_complete,
                    ip_is_disabled=ip_group.ip_is_disabled,
                    ip_is_published=ip_group.ip_is_published,
                    ip_duplicity=ip_group.ip_duplicity,
                    ip_duplicity_indexes=ip_group.ip_duplicity_indexes
                )

                # Create an object for the IP group tags
                ip_group_tags = []
                for tag in tags:
                    # Get the IP group tag object from the database based on the IP group tag ID
                    if tag.fk_ip_group_id == ip_group.ip_group_id:
                        ip_group_tag = session.query(IPGroupsTags).get(tag.fk_ip_group_tag_id)
                        ip_group_tags.append(
                            IPGroupsTagsEntity(
                                ip_group_tag_id=ip_group_tag.ip_group_tag_id,
                                ip_group_tag_name=ip_group_tag.ip_group_tag_name,
                                ip_group_tag_color=ip_group_tag.ip_group_tag_color,
                                ip_group_tag_text_color=ip_group_tag.ip_group_tag_text_color,
                                ip_group_tag_description=ip_group_tag.ip_group_tag_description
                            )
                        )

                # Append the IP group and its tags to the list
                ip_group_tags_list.append((ip_group_obj, ip_group_tags))

            # Return the list of IP groups and their tags
            return ip_group_tags_list
        except Exception as e:
            raise e

    @staticmethod
    def get_group_by_site(session, group_metadata: dict) -> list:
        """
        Get all blacklisted IP groups from the database by site
        :param group_metadata: The group metadata
        :param session: The database session
        :return: List of blacklisted IP groups
        """
        # List of group IP groups
        group_list = []

        # Get the router from the database based on the site ID
        router = session.query(Router).filter_by(fk_site_id=group_metadata['site_id']).first()

        # Get all IP segments from the database based on the router ID
        segments = session.query(IPSegment).filter(IPSegment.fk_router_id == router.router_id)
        segments_ids = [segment.ip_segment_id for segment in segments]

        # Get all grouped IP groups from the database based on the group name and IP segments
        group_site_list = session.query(IPGroups).filter(
            IPGroups.ip_group_name == group_metadata['group'],
            IPGroups.fk_ip_segment_id.in_(segments_ids)
        ).all()

        # Iterate on the grouped IP groups and create a list of group IP groups
        for ip_group in group_site_list:
            # Create the group IP group object
            ip_group_entity = IPGroupsEntity(
                ip_group_id=ip_group.ip_group_id,
                fk_ip_segment_id=ip_group.fk_ip_segment_id,
                ip_group_name=ip_group.ip_group_name,
                ip_group_type=ip_group.ip_group_type,
                ip_group_alias=ip_group.ip_group_alias,
                ip_group_description=ip_group.ip_group_description,
                ip_group_ip=ip_group.ip_group_ip,
                ip_group_mask=ip_group.ip_group_mask,
                ip_group_mac=ip_group.ip_group_mac,
                ip_group_mac_vendor=ip_group.ip_group_mac_vendor,
                ip_group_interface=ip_group.ip_group_interface,
                ip_group_comment=ip_group.ip_group_comment,
                ip_is_dhcp=ip_group.ip_is_dhcp,
                ip_is_dynamic=ip_group.ip_is_dynamic,
                ip_is_complete=ip_group.ip_is_complete,
                ip_is_disabled=ip_group.ip_is_disabled,
                ip_is_published=ip_group.ip_is_published,
                ip_duplicity=ip_group.ip_duplicity,
                ip_duplicity_indexes=ip_group.ip_duplicity_indexes
            )

            # Obtain tags for this IP group
            assigned_tags = session.query(IPGroupsToIPGroupsTags).filter_by(fk_ip_group_id=ip_group.ip_group_id).all()
            tags = [
                session.query(IPGroupsTags).get(tag.fk_ip_group_tag_id) for tag in assigned_tags
            ]

            # Create a list of tags for this IP group
            tags_entity = [
                IPGroupsTagsEntity(
                    tag.ip_group_tag_id,
                    tag.ip_group_tag_name,
                    tag.ip_group_tag_color,
                    tag.ip_group_tag_text_color,
                    tag.ip_group_tag_description
                ) for tag in tags
            ]

            # Append the group IP group object and its tags to the list
            group_list.append((ip_group_entity, tags_entity))

        # Return the list of group IP groups
        return group_list

    @staticmethod
    def get_available_authorized_by_site(session, metadata: dict) -> list:
        """
        Get all available authorized IP groups from the database by site
        :param session: The database session
        :param site_id: The site ID
        :return: List of available authorized IP groups
        """
        try:
            from models.ip_management.functions import IPAddressesFunctions

            # List of available authorized IP groups
            authorized_list = []

            # Get the router from the database based on the site ID
            router = session.query(Router).filter_by(fk_site_id=metadata['site_id']).first()

            # Get all IP segments from the database based on the router ID
            ip_segments = session.query(IPSegment).filter_by(
                fk_router_id=router.router_id
            ).all()

            # Iterate for each segment
            for ipx in ip_segments:
                # Verify is the segment is disabled
                if ipx.ip_segment_is_disabled is False:
                    # List of available and unavailable IP groups
                    a_list = []
                    u_list = []

                    # Get all available IP groups from the database based on the segment ID
                    available_ips = IPAddressesFunctions.get_available_ip_by_segment(session, ipx.ip_segment_id)
                    unavailable_ips = session.query(IPGroups).filter_by(fk_ip_segment_id=ipx.ip_segment_id).all()

                    # Iterate on the available and unavailable IP groups and create a list of available authorized IP groups
                    if unavailable_ips:
                        for ipy in unavailable_ips:
                            u_list.append([ipy.ip_group_id, ipy.ip_group_ip])

                    # Append the available and unavailable IP groups to the list
                    if available_ips:
                        a_list = available_ips



                    # Append the available authorized IP groups to the list
                    authorized_list.append(
                        {
                            f'{ipx.ip_segment_ip}/{ipx.ip_segment_mask}': {
                                'available': a_list,
                                'unavailable': u_list
                            }
                        }
                    )
                else:
                    # Append the available authorized IP groups to the list
                    authorized_list.append(
                        {
                            f'{ipx.ip_segment_ip}/{ipx.ip_segment_mask}': -1
                        }
                    )

            # Return the list of available authorized IP groups
            return authorized_list
        except Exception as e:
            raise e

    @staticmethod
    def get_count_ip_by_site(session, metadata: dict) -> list:
        """
        Get the count of private IP groups from the database by site
        :param session: The database session
        :param metadata: The metadata
        :return: List of available private IP groups
        """
        try:
            from models.ip_management.functions import IPAddressesFunctions

            # List of available private IP groups
            private_list = []

            # Get the router from the database based on the site ID
            router = session.query(Router).filter_by(fk_site_id=metadata['site_id']).first()

            # Get all IP segments from the database based on the router ID
            ip_segments = session.query(IPSegment).filter_by(
                fk_router_id=router.router_id,
                ip_segment_tag='PRIVATE_IP' if metadata['type'] == 'private' else 'PUBLIC_IP'
            ).all()

            # Iterate for each segment
            for ipx in ip_segments:
                # List of available and unavailable IP groups
                sum_u = 0
                sum_a = 0

                # Get all available IP groups from the database based on the segment ID
                available_ips = IPAddressesFunctions.get_available_ip_by_segment(session, ipx.ip_segment_id)
                unavailable_ips = session.query(IPGroups).filter_by(fk_ip_segment_id=ipx.ip_segment_id).all()

                # Iterate on the available and unavailable IP groups and create a list of available private IP groups
                if unavailable_ips:
                    sum_u = len(unavailable_ips)

                # Append the available and unavailable IP groups to the list
                if available_ips:
                    sum_a = len(available_ips)

                # Append the available private IP groups to the list
                private_list.append(
                    {
                        f'{ipx.ip_segment_ip}/{ipx.ip_segment_mask}': sum_u + sum_a
                    }
                )

            # Return the list of available private IP groups
            return private_list
        except Exception as e:
            raise e

    @staticmethod
    def get_assigned_ip_by_site(session, metadata: dict) -> list:
        """
        Get all available private IP groups from the database by site
        :param session: The database session
        :param site_id: The site ID
        :return: List of available private IP groups
        """
        try:
            from models.ip_management.functions import IPAddressesFunctions

            # List of available private IP groups
            private_list = []

            # Get the router from the database based on the site ID
            router = session.query(Router).filter_by(fk_site_id=metadata['site_id']).first()

            # Get all IP segments from the database based on the router ID
            if metadata['type']:
                ip_segments = session.query(IPSegment).filter_by(
                    fk_router_id=router.router_id,
                    ip_segment_tag='PRIVATE_IP' if metadata['type'] == 'private' else 'PUBLIC_IP'
                ).all()
            else:
                ip_segments = session.query(IPSegment).filter_by(fk_router_id=router.router_id).all()

            # Iterate for each segment
            for ipx in ip_segments:
                # List of available and unavailable IP groups
                u_list = []

                # Get all available IP groups from the database based on the segment ID
                unavailable_ips = session.query(IPGroups).filter_by(fk_ip_segment_id=ipx.ip_segment_id).all()

                # Iterate on the available and unavailable IP groups and create a list of available private IP groups
                if unavailable_ips:
                    for ipy in unavailable_ips:
                        u_list.append([ipy.ip_group_id, ipy.ip_group_ip])

                # Append the available private IP groups to the list
                private_list.append(
                    {
                        f'{ipx.ip_segment_ip}/{ipx.ip_segment_mask}': [
                            u[1] for u in u_list
                        ]
                    }
                )

            # Return the list of available private IP groups
            return private_list
        except Exception as e:
            raise e

    @staticmethod
    def get_available_ip_by_site(session, metadata: dict) -> list:
        """
        Get all available private IP groups from the database by site
        :param session: 
        :param metadata: 
        :return: 
        """
        try:
            from models.ip_management.functions import IPAddressesFunctions

            # List of available private IP groups
            private_list = []

            # Get the router from the database based on the site ID
            router = session.query(Router).filter_by(fk_site_id=metadata['site_id']).first()

            # Get all IP segments from the database based on the router ID
            ip_segments = session.query(IPSegment).filter_by(
                fk_router_id=router.router_id,
                ip_segment_tag='PRIVATE_IP' if metadata['type'] == 'private' else 'PUBLIC_IP'
            ).all()

            # Iterate for each segment
            for ipx in ip_segments:
                # List of available and unavailable IP groups
                a_list = []

                # Get all available IP groups from the database based on the segment ID
                available_ips = IPAddressesFunctions.get_available_ip_by_segment(session, ipx.ip_segment_id)

                # Iterate on the available and unavailable IP groups and create a list of available private IP groups
                if available_ips:
                    a_list = available_ips

                # Append the available private IP groups to the list
                private_list.append(
                    {
                        f'{ipx.ip_segment_ip}/{ipx.ip_segment_mask}': [
                            a for a in a_list
                        ]
                    }
                )

            # Return the list of available private IP groups
            return private_list
        except Exception as e:
            raise e

    @staticmethod
    def bulk_update_duplicity(session, ip_groups: list[IPGroupsEntity]) -> None:
        """
        Update the duplicity of a list of IP groups
        :param session: The database session
        :param ip_groups: The list of IP groups
        :return: None
        """
        try:
            # Create a list of IP Groups objects to update
            to_update = []

            # Iterate on the IP groups and update their duplicity in the database
            for ip_group in ip_groups:
                # Get the IP group from the database based on the IP group ID
                ip_group_x = session.query(IPGroups).get(ip_group.ip_group_id)

                # Update the IP group in the database
                ip_group_x.ip_duplicity = ip_group.ip_duplicity
                ip_group_x.ip_duplicity_indexes = ip_group.ip_duplicity_indexes

                # Add the IP group to the list
                to_update.append(ip_group_x)

            # Update the IP groups in the database
            session.bulk_save_objects(to_update)
        except Exception as e:
            raise e

    @staticmethod
    def bulk_delete_duplicity(session, ip_group_ids: list[int]) -> None:
        """
        Delete the duplicity of a list of IP groups
        :param session: The database session
        :param ip_group_ids: The list of IP group IDs
        :return: None
        """
        try:
            # Create a list of IP Groups objects to update
            to_update = []

            # Iterate on the IP groups and update their duplicity in the database
            for ip_group_id in ip_group_ids:
                # Get the IP group from the database based on the IP group ID
                ip_group_x = session.query(IPGroups).get(ip_group_id)

                # Update the IP group in the database
                ip_group_x.ip_duplicity = False
                ip_group_x.ip_duplicity_indexes = ''

                # Add the IP group to the list
                to_update.append(ip_group_x)

            # Update the IP groups in the database
            session.bulk_save_objects(to_update)
        except Exception as e:
            raise e

    @staticmethod
    def move_to_arps(session, ip_groups: list[IPGroupsEntity]) -> None:
        """
        Move a list of IP groups to ARP
        :param session: The database session
        :param ip_groups: The list of IP groups
        :return: None
        """

        try:
            # Import the ARP model
            from models.router_scan.models import ARP

            # Create a list of ARP objects to add to the database
            arps = []
            for ip_group in ip_groups:
                arps.append(ARP(
                    fk_ip_address_id=ip_group.fk_ip_segment_id,
                    arp_ip=ip_group.ip_group_ip,
                    arp_mac=ip_group.ip_group_mac,
                    arp_alias=ip_group.ip_group_alias,
                    arp_tag='Public IP' if ip_group.ip_group_type == 'public' else 'Private IP',
                    arp_interface=ip_group.ip_group_interface,
                    arp_is_dhcp=ip_group.ip_is_dhcp,
                    arp_is_invalid=False,
                    arp_is_dynamic=ip_group.ip_is_dynamic,
                    arp_is_complete=ip_group.ip_is_complete,
                    arp_is_disabled=ip_group.ip_is_disabled,
                    arp_is_published=ip_group.ip_is_published,
                    arp_duplicity=ip_group.ip_duplicity,
                    arp_duplicity_indexes=ip_group.ip_duplicity_indexes
                ))

            # Delete the IP groups from the database
            session.query(IPGroups).filter(IPGroups.ip_group_id.in_([ip_group.ip_group_id for ip_group in ip_groups])).delete(synchronize_session=False)

            # Add the ARP objects to the database
            session.bulk_save_objects(arps)
        except Exception as e:
            raise e

    @staticmethod
    def delete_duplicity_on_table(session) -> None:
        """
        Delete all duplicity from the IP groups table
        :param session: The database session
        :return: None
        """
        try:
            # Delete all IPs with duplicity from the database
            for i in session.query(IPGroups).filter(IPGroups.ip_duplicity == True).all():
                # Delete the IP group from the database
                session.delete(i)

                # Commit the changes
                session.commit()
        except Exception as e:
            raise e

    @staticmethod
    def change_duplicity_to_true(session, ip_group_ids: list[int]) -> None:
        """
        Change the duplicity of an IP group to True
        :param session: The database session
        :param ip_group_ids: The list of IP group IDs
        :return: None
        """

        try:
            # Iterate on the list of IP group IDs
            for ip_group_id in ip_group_ids:
                # Get the IP group from the database based on the IP group ID
                ip_group = session.query(IPGroups).get(ip_group_id)

                # Update the IP group in the database
                ip_group.ip_duplicity = True

                # Save updates
                session.commit()
        except Exception as e:
            raise e