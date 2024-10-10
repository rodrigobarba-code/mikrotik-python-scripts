import requests
from . import ip_management_bp
from entities.site import SiteEntity
from entities.region import RegionEntity
from entities.ip_segment import IPSegmentEntity
from app.functions import get_verified_jwt_header
from app.decorators import RequirementsDecorators as restriction
from flask import render_template, redirect, url_for, flash, request, jsonify, session

def get_regions() -> list:
    try:
        response = requests.get(
            'http://localhost:8080/api/private/regions/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                regions_list = [
                    RegionEntity(
                        region.get('region_id'),
                        region.get('region_name')
                    )
                    for region in response.json().get('regions')
                ]
                return regions_list
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve regions')
    except Exception as e:
        flash(str(e), 'danger')

def get_region_name_by_site(sites, regions, fk_region_id):
    region_dict = {region.region_id: region.region_name for region in regions}

    for site in sites:
        if site.fk_region_id == fk_region_id:
            return region_dict.get(fk_region_id)
    return None

def get_sites() -> list:
    try:
        response = requests.get(
            'http://localhost:8080/api/private/sites/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                sites_list = [
                    SiteEntity(
                        site.get('site_id'),
                        site.get('fk_region_id'),
                        '',
                        site.get('site_name'),
                        site.get('site_segment')
                    )
                    for site in response.json().get('sites')
                ]
                return sites_list
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve sites')
    except Exception as e:
        flash(str(e), 'danger')

def get_site_name(site_id, sites):
    for site in sites:
        if site.site_id == int(site_id):
            return site.site_name
    return None

def get_segment(segment_id: int):
    try:
        response = requests.get(
            f'http://localhost:8080/api/private/segment/{segment_id}',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id'),
                'segment_id': segment_id
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                segment = response.json().get('segment')
                return IPSegmentEntity(
                        segment.get('ip_segment_id'),
                        segment.get('fk_router_id'),
                        segment.get('ip_segment_ip'),
                        segment.get('ip_segment_mask'),
                        segment.get('ip_segment_network'),
                        segment.get('ip_segment_interface'),
                        segment.get('ip_segment_actual_iface'),
                        segment.get('ip_segment_tag'),
                        segment.get('ip_segment_comment'),
                        segment.get('ip_segment_is_invalid'),
                        segment.get('ip_segment_is_dynamic'),
                        segment.get('ip_segment_is_disabled')
                )
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve segment')
    except Exception as e:
        flash(str(e), 'danger')

def get_segments_by_site(site_id) -> list:
    try:
        response = requests.get(
            f'http://localhost:8080/api/private/segment/site/{site_id}',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id'),
                'site_id': site_id
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                segments_list = [
                    IPSegmentEntity(
                        segment.get('ip_segment_id'),
                        segment.get('fk_router_id'),
                        segment.get('ip_segment_ip'),
                        segment.get('ip_segment_mask'),
                        segment.get('ip_segment_network'),
                        segment.get('ip_segment_interface'),
                        segment.get('ip_segment_actual_iface'),
                        segment.get('ip_segment_tag'),
                        segment.get('ip_segment_comment'),
                        segment.get('ip_segment_is_invalid'),
                        segment.get('ip_segment_is_dynamic'),
                        segment.get('ip_segment_is_disabled')
                    )
                    for segment in response.json().get('segments')
                ]
                return segments_list
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve segments')
    except Exception as e:
        flash(str(e), 'danger')

@ip_management_bp.route('/', methods=['GET'])
@restriction.login_required  
@restriction.admin_required  
def ip_management():
    try:
        available_sites_obj = get_sites()
        available_regions_obj = get_regions()

        available_sites = []  
        available_regions = []  
        available_segments = []  

        for site in available_sites_obj:
            available_sites.append({
                'id': site.site_id,  
                'name': site.site_name,  
                'value': site.site_name,  
                'region': get_region_name_by_site(available_sites_obj, available_regions_obj, site.fk_region_id),
                'segment': site.site_segment,  
                'hidden': False
            })

            available_segments.append({
                'value': site.site_segment,  
                'segment': site.site_segment  
            })

        for region in available_regions_obj:
            available_regions.append({
                'id': region.region_id,  
                'name': region.region_name,  
                'value': region.region_name  
            })

        return render_template(
            'ip_management/ip_management.html',  
            available_segments=available_segments,  
            available_regions=available_regions,  
            available_sites=available_sites  
        )
    except Exception as e:  
        flash(str(e), 'danger')  
        return redirect(url_for('ip_management.ip_management'))

@ip_management_bp.route('/options/<site_id>', methods=['GET'])
@restriction.login_required  
@restriction.admin_required  
def ip_management_options_by_site(site_id):
    try:
        site_id = site_id  
        site_name = get_site_name(site_id, get_sites())
        return render_template(
            'ip_management/ip_management_options.html',  
            site_name=site_name,  
            site_id=site_id  
        )
    except Exception as e:
        flash(str(e), 'danger')  
        return redirect(url_for('ip_management.ip_management'))  

@ip_management_bp.route('/segments/<int:site_id>', methods=['GET'])
@restriction.login_required  
@restriction.admin_required  
def ip_segment(site_id):
    try:
        site_id = site_id  
        site_name = get_site_name(site_id, get_sites())
        ip_segment_list = get_segments_by_site(site_id)
        return render_template(
            'ip_management/ip_segments.html',  
            ip_segment_list=ip_segment_list,  
            site_name=site_name,  
            site_id=site_id  
        )
    except Exception as e:  
        flash(str(e), 'danger')  
        return redirect(url_for('ip_management.ip_segment', site_id=site_id))

@ip_management_bp.route('/segments/delete/<int:segment_id>/<int:site_id>', methods=['GET'])
@restriction.login_required  
@restriction.admin_required  
def delete_segment(segment_id, site_id):
    try:  
        response = requests.delete(
            f'http://localhost:8080/api/private/segment/{segment_id}',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id'),
                'segment_id': segment_id
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('IP Segment deleted successfully', 'success')
                return redirect(url_for('ip_management.ip_segment', site_id=site_id))
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete IP Segment')
    except Exception as e:  
        flash(str(e), 'danger')  
        return redirect(url_for('ip_management.ip_segment', site_id=site_id))

@ip_management_bp.route('/segments/delete/bulk', methods=['POST'])
@restriction.login_required  
@restriction.admin_required  
def bulk_delete_segment():
    data = request.get_json()
    segments_ids = data.get('items_ids', [])
    try:
        response = requests.delete(
            'http://localhost:8080/api/private/segments/bulk/',
            json={'segments_ids': segments_ids},
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id')
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flag = response.json().get('count_flag')
                flash(f'{flag} segments deleted successfully', 'success')

                return jsonify({'message': f'{flag} segments deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete segments')
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': 'Failed to delete segments', 'error': str(e)}), 500

@ip_management_bp.route('/segments/delete/all/<int:site_id>', methods=['POST'])
@restriction.login_required  
@restriction.admin_required  
def delete_segments(site_id):
    try:
        response = requests.delete(
            f'http://localhost:8080/api/private/segments/site/{site_id}',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('All IP Segments deleted successfully', 'success')
                return jsonify({'message': 'All IP Segments deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
    except Exception as e:  
        flash(str(e), 'danger')  
        return jsonify({'message': 'Failed to delete all IP Segments', 'error': str(e)}), 500

@ip_management_bp.route('/segment/details/', methods=['GET'])
@restriction.login_required  
@restriction.admin_required  
def get_ip_segment_details():
    try:
        id = request.args.get('id')
        segment = get_segment(int(id))

        return jsonify(
            [{
                'id': ['Identifier', segment.ip_segment_id],
                'router_id': ['Router ID', segment.fk_router_id],
                'ip': ['IP', segment.ip_segment_ip],
                'mask': ['Mask', segment.ip_segment_mask],
                'network': ['Network', segment.ip_segment_network],
                'interface': ['Interface', segment.ip_segment_interface],
                'actual_iface': ['Actual Interface', segment.ip_segment_actual_iface],
                'tag': ['Tag', segment.ip_segment_tag],
                'comment': ['Comment', segment.ip_segment_comment],
                'is_invalid': ['Is Invalid', segment.ip_segment_is_invalid],
                'is_dynamic': ['Is Dynamic', segment.ip_segment_is_dynamic],
                'is_disabled': ['Is Disabled', segment.ip_segment_is_disabled]
            }]
        ), 200
    except Exception as e:  
        return jsonify({'message': 'Failed to get router data', 'error': str(e)}), 500
