from .. import Base, SessionLocal
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
    def add_arp(arp: ARPEntity):
        session = SessionLocal()
        try:
            if (ARPFunctions.validate_arp_exists(
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
                session.commit()
            else:
                arp.validate_arp()  
                arp_obj = ARP.query.filter(
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
                session.commit()  
        except Exception as e:  
            session.rollback()  
            print(str(e))  

    @staticmethod
    def delete_arp(arp_id):
        session = SessionLocal()
        try:  
            arp = ARP.query.get(arp_id)  
            session.delete(arp)  
            session.commit()  
        except Exception as e:  
            session.rollback()  
            print(str(e))  

    @staticmethod
    def delete_all_arps():
        session = SessionLocal()
        try:
            ARP.query.delete()  
            session.commit()  
        except Exception as e:  
            session.rollback()  
            print(str(e))  

    @staticmethod
    def get_arp(arp_id):
        session = SessionLocal()
        try:  
            arp = ARP.query.get(arp_id)  
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
            print(str(e))  

    @staticmethod
    def get_arps():
        session = SessionLocal()
        try:  
            arps = ARP.query.all()  
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
            print(str(e))

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
    def add_arp_tag(arp_tag: ARPTag):
        session = SessionLocal()
        try:  
            
            if (ARPTags.query.filter(
                ARPTags.fk_arp_id == arp_tag.fk_arp_id,  
                ARPTags.arp_tag_value == arp_tag.arp_tag_value  
            ).first() is None):
                arp_tag_obj = ARPTags(  
                    fk_arp_id=arp_tag.fk_arp_id,  
                    arp_tag_value=arp_tag.arp_tag_value  
                )
                session.add(arp_tag_obj)  
                session.commit()  
        except Exception as e:  
            session.rollback()  
            print(str(e))  

    @staticmethod
    def delete_arp_tag(arp_tag_id):
        session = SessionLocal()
        try:  
            arp_tag = ARPTags.query.get(arp_tag_id)  
            session.delete(arp_tag)  
            session.commit()  
        except Exception as e:  
            session.rollback()  
            print(str(e))  

    @staticmethod
    def delete_all_arp_tags():
        session = SessionLocal()
        try:  
            ARPTags.query.delete()  
            session.commit()  
        except Exception as e:
            session.rollback()
            print(str(e))

    @staticmethod
    def delete_arp_tags(arp_id):
        session = SessionLocal()
        try:  
            ARPTags.query.filter(ARPTags.fk_arp_id == arp_id).delete()  
            session.commit()  
        except Exception as e:  
            session.rollback()  
            print(str(e))  

    @staticmethod
    def get_arp_tags(arp_id):
        try:  
            arp_tags = ARPTags.query.filter(ARPTags.fk_arp_id == arp_id).all()  
            obj_list = []  
            for arp_tag in arp_tags:  
                obj_list.append(arp_tag.arp_tag_value)  
            return obj_list  
        except Exception as e:  
            print(str(e))  

    @staticmethod
    def assign_first_tag():
        session = SessionLocal()
        try:
            arp_tags = ARPTag.get_tags()
            arps = ARP.query.all()
            for arp in arps:
                arp_item = ""
                if arp.arp_ip.startswith("10."):
                    arp_temp = ARPTag(
                        arp_tag_id=int(),  
                        fk_arp_id=arp.arp_id,  
                        arp_tag_value=arp_tags['INTERNAL_CONNECTION']  
                    )
                    ARPTags.add_arp_tag(arp_temp)  
                    arp_item = arp_tags['PRIVATE_IP']  
                else:
                    arp_item = arp_tags['PUBLIC_IP']
                arp_tag = ARPTag(
                    arp_tag_id=int(),  
                    fk_arp_id=arp.arp_id,  
                    arp_tag_value=arp_item  
                )
                ARPTags.add_arp_tag(arp_tag)
        except Exception as e:  
            session.rollback()  
            print(str(e))  
    

