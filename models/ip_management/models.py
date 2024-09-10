from .. import Base, SessionLocal
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey

from entities.ip_segment import IPSegmentTag, IPSegmentEntity

from models.routers.models import Router

from models.ip_management.functions import IPAddressesFunctions

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
    def add_ip_segment(ip_segment: IPSegmentEntity):
        session = SessionLocal()  
        try:  
            
            if (IPAddressesFunctions.validate_ip_segment_exists(
                ip_segment.ip_segment_ip,
                ip_segment.ip_segment_mask,
                ip_segment.ip_segment_interface
            )):
                
                ip_segment.validate_ip_segment()  
                ip_segment_obj = IPSegment(  
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
                session.add(ip_segment_obj)  
                session.commit()  
            
            else:
                ip_segment.validate_ip_segment()  
                ip_segment_obj = IPSegment.query.filter(
                    IPSegment.ip_segment_ip == ip_segment.ip_segment_ip,  
                    IPSegment.ip_segment_mask == ip_segment.ip_segment_mask,  
                    IPSegment.ip_segment_interface == ip_segment.ip_segment_interface  
                ).first()
                ip_segment_obj.fk_router_id = ip_segment.fk_router_id  
                ip_segment_obj.ip_segment_network = ip_segment.ip_segment_network  
                ip_segment_obj.ip_segment_interface = ip_segment.ip_segment_interface  
                ip_segment_obj.ip_segment_actual_iface = ip_segment.ip_segment_actual_iface  
                ip_segment_obj.ip_segment_tag = ip_segment.ip_segment_tag  
                ip_segment_obj.ip_segment_comment = ip_segment.ip_segment_comment  
                ip_segment_obj.ip_segment_is_invalid = ip_segment.ip_segment_is_invalid  
                ip_segment_obj.ip_segment_is_dynamic = ip_segment.ip_segment_is_dynamic  
                ip_segment_obj.ip_segment_is_disabled = ip_segment.ip_segment_is_disabled  
                session.commit()  
        except Exception as e:  
            session.rollback()  
            print(e)

    @staticmethod
    def delete_ip_segment(ip_segment_id):
        session = SessionLocal()  
        try:  
            ip_segment = IPSegment.query.get(ip_segment_id)  
            session.delete(ip_segment)  
            session.commit()  
        except Exception as e:  
            session.rollback()  
            print(e)

    @staticmethod
    def delete_all_ip_segments():
        session = SessionLocal()  
        try:  
            IPSegment.query.delete()  
            session.commit()  
        except Exception as e:
            session.rollback()
            print(e)

    @staticmethod
    def get_ip_segment(ip_segment_id):
        try:  
            ip_segment = IPSegment.query.get(ip_segment_id)  
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
            print(e)

    @staticmethod
    def get_ip_segments():
        try:  
            ip_segments = IPSegment.query.all()  
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
            print(e)

    @staticmethod
    def get_ip_segments_by_site_id(site_id):
        try:  
            router = Router.query.filter_by(fk_site_id=site_id).first()  
            ip_segments = IPSegment.query.filter_by(fk_router_id=router.router_id).all()  
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
            print(e)

    @staticmethod
    def get_ip_segments_by_router_id(router_id):
        try:  
            ip_segments = IPSegment.query.filter_by(fk_router_id=router_id).all()  
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
            print(e)