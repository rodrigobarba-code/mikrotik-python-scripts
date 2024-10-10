from app.blueprints.ip_management.routes import ip_segment
from .. import Base
from models.routers.models import Router
from entities.ip_segment import IPSegmentTag, IPSegmentEntity
from models.ip_management.functions import IPAddressesFunctions
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey

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
            from models.router_scan.models import ARP, ARPTags

            arps = session.query(ARP.arp_id).filter_by(fk_ip_address_id=ip_segment_id).all()
            arp_ids = [arp.arp_id for arp in arps]

            if arp_ids:
                session.query(ARPTags).filter(ARPTags.fk_arp_id.in_(arp_ids)).delete(synchronize_session=False)

                session.query(ARP).filter(ARP.arp_id.in_(arp_ids)).delete(synchronize_session=False)

            ip_segment = session.query(IPSegment).get(ip_segment_id)
            if ip_segment:
                session.delete(ip_segment)
        except Exception as e:
            raise e

    @staticmethod
    def delete_ip_segments(session):
        try:
            from models.router_scan.models import ARP, ARPTags

            session.query(ARPTags).delete()
            session.query(ARP).delete()

            session.query(IPSegment).delete()
        except Exception as e:
            raise e

    @staticmethod
    def delete_ip_segments_by_site(session, site_id):
        try:
            from models.router_scan.models import ARP, ARPTags

            routers = session.query(Router).filter_by(fk_site_id=site_id).all()

            ip_segments = session.query(IPSegment).filter(IPSegment.fk_router_id.in_([router.router_id for router in routers])).all()
            ip_segment_ids = [ip_segment.ip_segment_id for ip_segment in ip_segments]

            arps = session.query(ARP.arp_id).filter(ARP.fk_ip_address_id.in_(ip_segment_ids)).all()
            arp_ids = [arp.arp_id for arp in arps]

            if arp_ids:
                session.query(ARPTags).filter(ARPTags.fk_arp_id.in_(arp_ids)).delete(synchronize_session=False)
                session.query(ARP).filter(ARP.arp_id.in_(arp_ids)).delete(synchronize_session=False)

            session.query(IPSegment).filter(IPSegment.ip_segment_id.in_(ip_segment_ids)).delete(synchronize_session=False)
        except Exception as e:
            raise e

    @staticmethod
    def bulk_delete_ip_segments(session, segments_ids):
        try:
            from models.router_scan.models import ARP, ARPTags

            arps = session.query(ARP.arp_id).filter(ARP.fk_ip_address_id.in_(segments_ids)).all()
            arp_ids = [arp.arp_id for arp in arps]

            if arp_ids:
                session.query(ARPTags).filter(ARPTags.fk_arp_id.in_(arp_ids)).delete(synchronize_session=False)
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
