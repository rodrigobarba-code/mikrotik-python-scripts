from models.ip_management.models import IPSegment


class DashboardFunctions:
    def __init__(self):
        pass

    @staticmethod
    def get_assigned_ip_per_site(type: str) -> dict:
        # Import the model here to avoid circular imports
        from models.routers.models import Router
        from models.ip_management.models import IPGroups
        from utils.threading_manager import ThreadingManager

        try:
            # Initialize the return dictionary
            return_dict = {}

            # Get all sites
            tmp = ThreadingManager().run_thread(
                Site.get_sites,
                'r'
            )

            # Get Tuple List for all sites
            site_list = [
                (site.site_id, site.site_name)
                for site in tmp
            ]

            for site_id, site_name in site_list:
                # Verify if the site has a router

                if ThreadingManager().run_thread(
                        Router.verify_if_router_has_segments,
                        'rx',
                        site_id
                ) is True:
                    # Initialize the list by segment
                    by_segment = []
                    total_count_by_site = 0

                    metadata = {
                        'site_id': site_id,
                        'type': type
                    }

                    # Get the count of private IP groups from the database by site
                    count_by_site = ThreadingManager().run_thread(
                        IPGroups.get_count_ip_by_site,
                        'rx',
                        metadata
                    )

                    # Get available IP Groups
                    available_ip_groups = ThreadingManager().run_thread(
                        IPGroups.get_assigned_ip_by_site,
                        'rx',
                        metadata
                    )

                    # Initialize total count of assigned IPs
                    total_assigned_ips = 0

                    # Iterate for each IP element
                    for segment in available_ip_groups:
                        # Get key of the segment
                        key = list(segment.keys())[0]

                        # Get the value of the segment
                        value = list(segment.values())[0]

                        # Append the segment to the list
                        total_assigned_ips += len(value)

                        # Append the count of all IPs to the segment
                        count = [
                            count[key]
                            for count in count_by_site
                            if list(count.keys())[0] == key
                        ][0]

                        total_count_by_site += count

                        # Append the segment to the list
                        by_segment.append(
                            {
                                f'{key}': {
                                    'quantity': len(value),
                                    'percentage': len(value) / count * 100
                                }
                            }
                        )

                    # Append the site to the return dictionary
                    return_dict[site_name] = {
                        'quantity': total_assigned_ips,
                        'percentage': total_assigned_ips / total_count_by_site * 100,
                        'no_segments': len(by_segment),
                        'by_segment': by_segment
                    }
                else:
                    pass

            # Return the dictionary
            return return_dict
        except Exception as e:
            raise e

    @staticmethod
    def get_available_ip_per_site(type: str) -> dict:
        # Import the model here to avoid circular imports
        from models.routers.models import Router
        from models.ip_management.models import IPGroups
        from utils.threading_manager import ThreadingManager

        try:
            # Initialize the return dictionary
            return_dict = {}

            # Get all sites
            tmp = ThreadingManager().run_thread(
                Site.get_sites,
                'r'
            )

            # Get Tuple List for all sites
            site_list = [
                (site.site_id, site.site_name)
                for site in tmp
            ]

            for site_id, site_name in site_list:
                # Verify if the site has a router
                if ThreadingManager().run_thread(
                    Router.verify_if_router_has_segments,
                    'rx',
                    site_id
                ) is True:
                    # Initialize the list by segment and total count by site
                    by_segment = []
                    total_count_by_site = 0

                    metadata = {
                        'site_id': site_id,
                        'type': type
                    }

                    # Get the count of private IP groups from the database by site
                    count_by_site = ThreadingManager().run_thread(
                        IPGroups.get_count_ip_by_site,
                        'rx',
                        metadata
                    )

                    # Get available IP Groups
                    available_ip_groups = ThreadingManager().run_thread(
                        IPGroups.get_available_ip_by_site,
                        'rx',
                        metadata
                    )

                    # Initialize total count of assigned IPs
                    total_available_ips = 0

                    # Iterate for each IP element
                    for segment in available_ip_groups:
                        # Get key of the segment
                        key = list(segment.keys())[0]

                        # Get the value of the segment
                        value = list(segment.values())[0]

                        # Append the segment to the list
                        total_available_ips += len(value)

                        # Append the count of all IPs to the segment
                        count = 0
                        for count in count_by_site:
                            if list(count.keys())[0] == key:
                                count = count[key]
                                break

                        total_count_by_site += count

                        # Append the segment to the list
                        by_segment.append(
                            {
                                f'{key}': {
                                    'quantity': len(value),
                                    'percentage': len(value) / count * 100
                                }
                            }
                        )

                    # Append the site to the return dictionary
                    return_dict[site_name] = {
                        'quantity': total_available_ips,
                        'percentage': total_available_ips / total_count_by_site * 100,
                        'no_segments': len(by_segment),
                        'by_segment': by_segment
                    }
                else:
                    pass

            # Return the dictionary
            return return_dict
        except Exception as e:
            raise e

    @staticmethod
    def get_duplicated_ip_with_indexes() -> dict:
        # Import the model here to avoid circular imports
        from models.router_scan.models import ARP
        from utils.threading_manager import ThreadingManager

        try:
            # Initialize the return dictionary
            return_dict = {}

            # Get all the ARPs on the database
            arps = ThreadingManager().run_thread(
                ARP.get_arps,
                'r'
            )

            # Iterate for each ARP element
            for arp in arps:
                # Get the ARP IP
                ip = arp.arp_ip

                # Verify if the IP is already in the dictionary
                if ip in return_dict.keys():
                    # Append the index to the dictionary
                    return_dict[ip].append(arp.arp_duplicity_indexes)
                else:
                    # Initialize the list with the index
                    return_dict[ip] = [arp.arp_duplicity_indexes]

            # Return the dictionary
            return return_dict
        except Exception as e:
            raise e

    @staticmethod
    def get_total_ips_on_database() -> dict:
        # Import the model here to avoid circular imports
        from models.router_scan.models import ARP
        from models.ip_management.models import IPGroups
        from utils.threading_manager import ThreadingManager

        try:
            # Get all ARP on the database
            arps = ThreadingManager().run_thread(
                ARP.get_arps,
                'r'
            )

            # Get all IP Groups on the database
            ip_groups = ThreadingManager().run_thread(
                IPGroups.get_ip_groups,
                'r'
            )

            # Return the dictionary
            return {
                'count_arps': len(arps),
                'count_ip_groups': len(ip_groups),
                'total': len(arps) + len(ip_groups)
            }
        except Exception as e:
            raise e

    @staticmethod
    def get_total_segments_per_site() -> dict:
        # Import the model here to avoid circular imports
        from models.sites.models import Site
        from models.routers.models import Router
        from utils.threading_manager import ThreadingManager

        try:
            # Initialize the return dictionary
            total = 0
            return_dict = {}

            # Get all sites
            tmp = ThreadingManager().run_thread(
                Site.get_sites,
                'r'
            )

            # Get Tuple List for all sites
            site_list = [
                (site.site_id, site.site_name)
                for site in tmp
            ]

            # Get all segments
            total_segments = len(
                ThreadingManager().run_thread(
                    IPSegment.get_ip_segments,
                    'r'
                )
            )

            for site_id, site_name in site_list:
                # Verify if the site has a router
                if ThreadingManager().run_thread(
                    Router.verify_if_router_has_segments,
                    'rx',
                    site_id
                ) is True:
                    # Get all the Segments from the database by site
                    segments = ThreadingManager().run_thread(
                        IPSegment.get_ip_segments_by_site_id,
                        'rx',
                        site_id
                    )

                    # Append the site to the return dictionary
                    return_dict[site_name] = {
                        'quantity': len(segments),
                        'percentage': len(segments) / total_segments * 100
                    }
                else:
                    pass

            # Return the dictionary
            return_dict['total'] = total_segments
            return return_dict
        except Exception as e:
            raise e
