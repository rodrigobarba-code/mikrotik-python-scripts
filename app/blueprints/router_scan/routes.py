import requests
from . import scan_bp
from app.functions import get_verified_jwt_header
from app.decorators import RequirementsDecorators as restriction
from flask import render_template, request, redirect, url_for, flash, session, jsonify

@scan_bp.route('/', methods=['GET', 'POST'])
def scan():
    arp_list = []
    response = requests.get(
        'http://localhost:8080/api/private/arps/essential/',
        headers=get_verified_jwt_header(),
        params={'user_id': session.get('user_id')}
    )
    if response.status_code == 200:
        if response.json().get('backend_status') == 200:
            arp_list = response.json().get('arps')
        else:
            raise Exception(response.json().get('message'))
    elif response.status_code == 500:
        raise Exception('Failed to retrieve sites')

    return render_template(
        'router_scan/scan.html',  
        arp_list=arp_list
    )

@scan_bp.route('/delete/<arp_id>', methods=['GET'])
@restriction.login_required  
@restriction.admin_required  
def delete_arp_ip(arp_id):
    try:  
        response = requests.delete(
            f'http://localhost:8080/api/private/arp/{arp_id}',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id'),
                'arp_id': arp_id
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('ARP IP Deleted Successfully', 'success')
                return redirect(url_for('router_scan.scan'))
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete ARP IP')
    except Exception as e:  
        flash(str(e), 'danger')  
    return redirect(url_for('router_scan.scan'))

@scan_bp.route('/delete/bulk', methods=['POST'])
@restriction.login_required  
@restriction.admin_required  
def bulk_delete_arp_ips():
    data = request.get_json()
    arps_ids = data.get('items_ids', [])  
    try:
        response = requests.delete(
            'http://localhost:8080/api/private/arps/bulk/',
            json={'arps_ids': arps_ids},
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id')
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flag = response.json().get('count_flag')
                flash(f'{flag} Routers deleted successfully', 'success')

                return jsonify({'message': f'{flag} routers deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete routers')
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': 'Failed to delete routers', 'error': str(e)}), 500

@scan_bp.route('/delete/all', methods=['POST'])
@restriction.login_required  
@restriction.admin_required  
def delete_all_arps_ips():
    try:  
        response = requests.delete(
            'http://localhost:8080/api/private/arps/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('ARP IPs Deleted Successfully', 'success')
                return jsonify({'message': 'ARP IPs deleted successfully'}), 200
            else:
                return jsonify({'message': response.json().get('message')}), 400
        elif response.status_code == 500:
            return jsonify({'message': 'Failed to delete ARP IPs'}), 500
    except Exception as e:  
        flash(str(e), 'danger')  
        return jsonify({'message': 'Failed to delete ARP IPs', 'error': str(e)}), 500

@scan_bp.route('/get_scan_details/', methods=['GET'])
def get_scan_details():
    try:
        arp_id = request.args.get('id')
        response = requests.get(
        f'http://localhost:8080/api/private/arp/essential/{arp_id}',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id'),
                'arp_id': arp_id
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                arp_item = response.json().get('arp')
                segment = arp_item.get('segment')
                arp_tags = arp_item.get('tag')
                return jsonify([{
                    'id': ["Identifier", arp_item['id']],
                    'segment': ["IP Segment", segment],
                    'ip': ["ARP IP", arp_item['ip']],
                    'mac': ["ARP MAC", arp_item['mac']],
                    'alias': ["ARP Alias", arp_item['alias']],
                    'tags': arp_tags,
                    'arp_interface': ["ARP Interface", arp_item['interface']],
                    'arp_is_dhcp': ["ARP is DHCP?", arp_item['is_dhcp']],
                    'arp_is_invalid': ["ARP is Invalid?", arp_item['is_invalid']],
                    'arp_is_dynamic': ["ARP is Dynamic?", arp_item['is_dynamic']],
                    'arp_is_complete': ["ARP is Complete?", arp_item['is_complete']],
                    'arp_is_disabled': ["ARP is Disabled?", arp_item['is_disabled']],
                    'arp_is_published': ["ARP is Published?", arp_item['is_published']]
                }]), 200
            else:
                return jsonify({'message': response.json().get('message')}), 400
        elif response.status_code == 500:
            return jsonify({'message': 'Failed to get ARP details'}), 500
    except Exception as e:  
        return jsonify({'message': 'Failed to get ARP details', 'error': str(e)}), 500
