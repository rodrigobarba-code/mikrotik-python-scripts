class DashboardFunctions:
    def __init__(self):
        pass

    @staticmethod
    def get_assigned_ip_per_site(type: str) -> dict:
        # Import the model here to avoid circular imports
        from models.sites.models import Site
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
                    IPGroups.get_available_ip_by_site,
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

            # Return the dictionary
            return return_dict
        except Exception as e:
            raise e
