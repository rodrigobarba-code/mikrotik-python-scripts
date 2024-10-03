import ipaddress

class FindIPSegment:
    def __init__(
        self,
        session=None,
    ):
        self.session = session

    def get_session(self):
        return self.session

    def set_session(self, session):
        self.session = session

    @staticmethod
    def find(ip_segments, arp_ip) -> list:
        """
        Find the IP Segment of the ARP IP
        :param ip_segments: The list of IP Segments
        :param arp_ip: The ARP IP
        :return: A list with the result of the find
        """
        try:
            # Convert the ARP IP to an IP Address object
            ip = ipaddress.ip_address(arp_ip)

            # Iterate over the IP Segments
            for segment in ip_segments:
                # Check if the mask is /32 (special case)
                if segment.ip_segment_mask == '32':
                    # Compare the ARP IP directly with the segment's IP
                    if ip == ipaddress.ip_address(segment.ip_segment_ip) or ip == ipaddress.ip_address(segment.ip_segment_network):
                        # print(f"Found IP {arp_ip} as a /32 match with Segment ID {segment.ip_segment_id}")
                        return [True, int(segment.ip_segment_id)]
                else:
                    # Create a network object with the IP and Mask for non /32 networks
                    network_str = f"{segment.ip_segment_ip}/{segment.ip_segment_mask}"
                    network = ipaddress.ip_network(network_str, strict=False)

                    # Debugging: Print to see if networks are being constructed correctly
                    # print(f"Checking IP: {arp_ip} in Network: {network_str}")

                    # Check if the IP is in the network
                    if ip in network:
                        # print(f"Found IP {arp_ip} in Network {network_str} with Segment ID {segment.ip_segment_id}")
                        return [True, int(segment.ip_segment_id)]

            # Return False and None if the IP Segment was not found
            # print(f"Could not find IP {ip} in any IP Segment")
            return [False, None]

        except Exception as e:
            raise Exception(f"An error occurred while finding the IP Segment: {str(e)}")

