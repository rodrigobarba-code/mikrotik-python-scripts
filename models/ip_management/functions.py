class IPAddressesFunctions:
    def __init__(self):  
        pass

    @staticmethod
    def validate_ip_segment_exists(session, ip_segment_ip, ip_segment_mask, ip_segment_interface):
        try:
            # Importing here to avoid circular imports
            from models.ip_management.models import IPSegment

            # Check if the IP segment exists in the database
            ip_segment = session.query(IPSegment).filter(
                IPSegment.ip_segment_ip == ip_segment_ip,
                IPSegment.ip_segment_mask == ip_segment_mask,
                IPSegment.ip_segment_interface == ip_segment_interface
            ).first()

            # If the IP segment exists, verify if the data is the same
            if ip_segment:
                # If the data is different, return True, else return False
                if ip_segment_ip != ip_segment.ip_segment_ip and ip_segment_mask != ip_segment.ip_segment_mask and ip_segment_interface != ip_segment.ip_segment_interface:
                    return True
                return False
            else:
                return True
        except Exception as e:
            print(str(e))

    @staticmethod
    def delete_ip_segments(session, ip_data: dict) -> None:
        from utils.threading_manager import ThreadingManager
        try:
            # Importing here to avoid circular imports
            from sqlalchemy import delete
            from models.ip_management.models import IPSegment

            # Create a list of tuples with the IP segments obtained from the router
            r_segment_list_real = [
                (router_segment.ip_segment_ip,
                 router_segment.ip_segment_mask,
                 router_segment.ip_segment_interface)
                for router_segment in ip_data['ip_list']
                if router_segment.fk_router_id == ip_data['router_id']
            ]

            # Create a list of IP segments from the database
            r_segments_list_db = [
                ip_segment for ip_segment in session.query(IPSegment).filter(
                    IPSegment.fk_router_id == ip_data['router_id']
                ).all()
            ]

            # Create a list for all IP segments that need to be deleted
            segments_to_delete = []

            # Validate if the IP segment exists in the database but not in the router
            if r_segment_list_real:
                for r_segment in r_segments_list_db:
                    # If the IP segment exists in the database but not in the router, add it to the list of segments to delete
                    if (r_segment.ip_segment_ip, r_segment.ip_segment_mask, r_segment.ip_segment_interface) not in r_segment_list_real:
                        segments_to_delete.append(r_segment)

            # If there are segments to delete, delete them
            if segments_to_delete:
                # Create a list with the IDs of the segments to delete
                segments_ids_to_delete = [segment.ip_segment_id for segment in segments_to_delete]

                # Delete the segments
                ThreadingManager().run_thread(IPSegment.bulk_delete_ip_segments, 'w', segments_ids_to_delete)
                print('IP segments deleted: ' + str(len(segments_ids_to_delete)))
            else:
                print('No segments to delete.')
        except Exception as e:  
            print('Error on deleting IP segments: ' + str(e))

    @staticmethod
    def determine_ip_segment_tag(ip_segment_ip: str) -> str:
        try:
            from entities.ip_segment import IPSegmentTag
            from models.ip_management.models import IPSegment

            if ip_segment_ip.startswith("10."):
                return IPSegmentTag['PRIVATE_IP'].value
            else:
                return IPSegmentTag['PUBLIC_IP'].value
        except Exception as e:  
            raise e

    @staticmethod
    def validate_ip_group_exists(session, ip_group_ip, ip_group_mask, ip_group_interface):
        try:
            # Importing here to avoid circular imports
            from models.ip_management.models import IPGroups

            # Check if the IP group exists in the database
            ip_group = session.query(IPGroups).filter(
                IPGroups.ip_group_ip == ip_group_ip,
                IPGroups.ip_group_mask == ip_group_mask,
                IPGroups.ip_group_interface == ip_group_interface
            ).first()

            # If the IP group exists, verify if the data is the same
            if ip_group:
                # If the data is different, return True, else return False
                if ip_group_ip != ip_group.ip_group_ip and ip_group_mask != ip_group.ip_group_mask and ip_group_interface != ip_group.ip_group_interface:
                    return True
                return False
            else:
                return True
        except Exception as e:
            print(str(e))