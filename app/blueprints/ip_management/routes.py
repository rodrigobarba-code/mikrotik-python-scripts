import requests
from . import ip_management_bp
from entities.site import SiteEntity
from entities.region import RegionEntity
from entities.ip_groups import IPGroupsEntity, IPGroupsTagsEntity
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
                'tags': ['Public IP' if segment.ip_segment_tag == 'PUBLIC_IP' else 'Private IP'],
                'comment': ['Comment', segment.ip_segment_comment],
                'is_invalid': ['Is Invalid', segment.ip_segment_is_invalid],
                'is_dynamic': ['Is Dynamic', segment.ip_segment_is_dynamic],
                'is_disabled': ['Is Disabled', segment.ip_segment_is_disabled]
            }]
        ), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get router data', 'error': str(e)}), 500


@ip_management_bp.route('/ip/group/details/', methods=['GET'])
def get_ip_group_details():
    try:
        ip_group_id = request.args.get('id')
        response = requests.get(
            f'http://localhost:8080/api/private/ip/group/{ip_group_id}',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id'),
                    'ip_group_id': ip_group_id
                    }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                blacklist_obj = response.json().get('ip_group')
                return jsonify([{
                    'id': ['Identifier', blacklist_obj.get('ip_group_id')],
                    'name': ['Group Name', 'Blacklist' if blacklist_obj.get(
                        'ip_group_name') == 'blacklist' else 'Authorized'],
                    'type': ['IP Type', blacklist_obj.get('ip_group_type')],
                    'alias': ['Alias', blacklist_obj.get('ip_group_alias')],
                    'description': ['Description', blacklist_obj.get('ip_group_description')],
                    'ip': ['IP', blacklist_obj.get('ip_group_ip')],
                    'mask': ['Mask', blacklist_obj.get('ip_group_mask')],
                    'mac': ['MAC', blacklist_obj.get('ip_group_mac')],
                    'mac_vendor': ['MAC Vendor', blacklist_obj.get('ip_group_mac_vendor')],
                    'interface': ['Interface', blacklist_obj.get('ip_group_interface')],
                    'comment': ['Comment', blacklist_obj.get('ip_group_comment')],
                    'ip_is_dhcp': ['IP is DHCP', blacklist_obj.get('ip_is_dhcp')],
                    'ip_is_dynamic': ['IP is Dynamic', blacklist_obj.get('ip_is_dynamic')],
                    'ip_is_complete': ['IP is Complete', blacklist_obj.get('ip_is_complete')],
                    'ip_is_disabled': ['IP is Disabled', blacklist_obj.get('ip_is_disabled')],
                    'ip_is_published': ['IP is Published', blacklist_obj.get('ip_is_published')],
                    'ip_duplicity': ['IP Duplicity', blacklist_obj.get('ip_duplicity')],
                    'tags': ['Tags', blacklist_obj.get('ip_group_tags')],

                }]), 200
            else:
                return jsonify({'message': response.json().get('message')}), 500
        elif response.status_code == 500:
            return jsonify({'message': 'Failed to get IP Group details'}), 500
    except Exception as e:
        return jsonify({'message': 'Failed to get IP Group details', 'error': str(e)}), 500


def get_blacklist(site_id: int) -> list:
    try:
        response = requests.get(
            f'http://localhost:8080/api/private/blacklist/{site_id}',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id'),
                'site_id': site_id
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                return response.json().get('blacklist')
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve blacklist')
    except Exception as e:
        flash(str(e), 'danger')
        return []


@ip_management_bp.route('/blacklist/<int:site_id>', methods=['GET'])
@restriction.login_required
@restriction.admin_required
def blacklist(site_id: int):
    try:
        site_name = get_site_name(site_id, get_sites())
        blacklist_list = get_blacklist(site_id)
        return render_template(
            'ip_management/ip_groups.html',
            site_name=site_name,
            site_id=site_id,
            groups=blacklist_list,
            is_blacklist=True
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('ip_management.ip_management'))


def get_authorized(site_id: int) -> list:
    try:
        response = requests.get(
            f'http://localhost:8080/api/private/ip/authorized/{site_id}',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id'),
                'site_id': site_id
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                return response.json().get('authorized')
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve authorized')
    except Exception as e:
        flash(str(e), 'danger')
        return []


@ip_management_bp.route('/authorized/<int:site_id>', methods=['GET'])
@restriction.login_required
@restriction.admin_required
def authorized(site_id: int):
    try:
        site_name = get_site_name(site_id, get_sites())
        authorized_list = get_authorized(site_id)
        return render_template(
            'ip_management/ip_groups.html',
            site_name=site_name,
            site_id=site_id,
            groups=authorized_list,
            is_blacklist=False
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('ip_management.ip_management'))


@ip_management_bp.route('/blacklist/delete/bulk', methods=['POST'])
@restriction.login_required
@restriction.admin_required
def bulk_delete_blacklist():
    data = request.get_json()
    blacklist_ids = data.get('items_ids', [])
    try:
        response = requests.delete(
            'http://localhost:8080/api/private/blacklist/bulk/',
            json={'blacklist_ids': blacklist_ids},
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


@ip_management_bp.route('/ip/group/delete/<int:ip_group_id>/<int:site_id>', methods=['GET'])
@restriction.login_required
@restriction.admin_required
def delete_ip_group(ip_group_id, site_id):
    try:
        response = requests.delete(
            f'http://localhost:8080/api/private/ip/group/{ip_group_id}',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id'),
                'ip_group_id': ip_group_id
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('IP Group deleted successfully', 'success')
                return redirect(url_for('ip_management.blacklist', site_id=site_id))
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete IP Group')
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('ip_management.blacklist', site_id=site_id))


@ip_management_bp.route('/ip/group/transfer/authorized/<int:ip_group_id>/<int:site_id>', methods=['GET'])
@restriction.login_required
@restriction.admin_required
def transfer_to_authorized(ip_group_id, site_id):
    try:
        response = requests.put(
            f'http://localhost:8080/api/private/blacklist/move/to/authorized/{ip_group_id}',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id'),
                'ip_group_id': ip_group_id
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('IP Group transferred successfully', 'success')
                return redirect(url_for('ip_management.blacklist', site_id=site_id))
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to transfer IP Group')
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('ip_management.blacklist', site_id=site_id))


@ip_management_bp.route('/ip/group/delete/bulk', methods=['POST'])
@restriction.login_required
@restriction.admin_required
def bulk_delete_ip_group():
    data = request.get_json()
    ip_group_ids = data.get('items_ids', [])
    try:
        response = requests.delete(
            'http://localhost:8080/api/private/ip/groups/bulk/',
            json={'ip_groups_ids': ip_group_ids},
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id')
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flag = response.json().get('count_flag')
                flash(f'{flag} IP Groups deleted successfully', 'success')

                return jsonify({'message': f'{flag} IP Groups deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete IP Groups')
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': 'Failed to delete IP Groups', 'error': str(e)}), 500


@ip_management_bp.route('/ip/group/delete/all/<int:site_id>/<is_blacklist>', methods=['POST'])
@restriction.login_required
@restriction.admin_required
def delete_ip_groups(site_id, is_blacklist):
    try:
        if is_blacklist is True:
            url = f'http://localhost:8080/api/private/blacklist/site/{site_id}'
        else:
            url = f'http://localhost:8080/api/private/ip/authorized/site/{site_id}'

        response = requests.delete(
            url,
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('All IP Groups deleted successfully', 'success')
                return jsonify({'message': 'All IP Groups deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': 'Failed to delete all IP Groups', 'error': str(e)}), 500


def get_tags():
    try:
        response = requests.get(
            'http://localhost:8080/api/private/ip/groups/tags/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                tags_list = [
                    IPGroupsTagsEntity(
                        tag.get('ip_group_tag_id'),
                        tag.get('ip_group_tag_name'),
                        tag.get('ip_group_tag_color'),
                        tag.get('ip_group_tag_text_color'),
                        tag.get('ip_group_tag_description')
                    )
                    for tag in response.json().get('ip_groups_tags')
                ]
                if tags_list is None:
                    return []
                return tags_list
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve tags')
    except Exception as e:
        flash(str(e), 'danger')
        return []


def get_tag(tag_id: int) -> IPGroupsTagsEntity:
    try:
        response = requests.get(
            f'http://localhost:8080/api/private/ip/groups/tags/{tag_id}',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id'),
                'ip_group_tag_id': tag_id
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                tag = response.json().get('ip_group_tag')
                return IPGroupsTagsEntity(
                    tag.get('ip_group_tag_id'),
                    tag.get('ip_group_tag_name'),
                    tag.get('ip_group_tag_color'),
                    tag.get('ip_group_tag_text_color'),
                    tag.get('ip_group_tag_description')
                )
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve tag')
    except Exception as e:
        flash(str(e), 'danger')
        return None


@ip_management_bp.route('/ip/group/tags/', methods=['GET'])
@restriction.login_required
@restriction.admin_required
def ip_group_tags():
    try:
        return render_template(
            'ip_management/ip_groups_tags.html',
            tags=get_tags()
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('ip_management.ip_management'))


@ip_management_bp.route('/ip/group/tags/add/', methods=['GET', 'POST'])
@restriction.login_required
@restriction.admin_required
def add_ip_group_tag():
    try:
        if request.method == 'POST':
            tag_name = request.form.get('tag_name')
            tag_color = request.form.get('tag_color')
            tag_text_color = request.form.get('tag_text_color')
            tag_description = request.form.get('tag_description')
            response = requests.post(
                'http://localhost:8080/api/private/ip/groups/tag/',
                headers=get_verified_jwt_header(),
                params={
                    'user_id': session.get('user_id'),
                    'x_ip_group_tag_name': tag_name,
                    'x_ip_group_tag_color': tag_color,
                    'x_ip_group_tag_text_color': tag_text_color,
                    'x_ip_group_tag_description': tag_description
                }
            )
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    flash('Tag added successfully', 'success')
                    return redirect(url_for('ip_management.ip_group_tags'))
                else:
                    raise Exception(response.json().get('message'))
            elif response.status_code == 500:
                raise Exception('Failed to add tag')
        return render_template(
            'ip_management/form_ip_groups_tags.html',
            tag=None
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('ip_management.ip_group_tags'))

@ip_management_bp.route('/ip/group/tags/update/<int:tag_id>', methods=['GET', 'POST'])
@restriction.login_required
@restriction.admin_required
def update_ip_group_tag(tag_id):
    try:
        tag_obj = get_tag(tag_id)
        if request.method == 'POST':
            response = requests.put(
                f'http://localhost:8080/api/private/ip/groups/tag/{tag_id}',
                headers=get_verified_jwt_header(),
                params={
                    'user_id': session.get('user_id'),
                    'ip_group_tag_id': tag_id,
                    'ip_group_tag_name': request.form.get('tag_name'),
                    'ip_group_tag_color': request.form.get('tag_color'),
                    'ip_group_tag_text_color': request.form.get('tag_text_color'),
                    'ip_group_tag_description': request.form.get('tag_description')
                }
            )
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    flash('Tag updated successfully', 'success')
                    return redirect(url_for('ip_management.ip_group_tags'))
                else:
                    raise Exception(response.json().get('message'))
            elif response.status_code == 500:
                raise Exception('Failed to update tag')
        return render_template(
            'ip_management/form_ip_groups_tags.html',
            tag_obj=tag_obj
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('ip_management.ip_group_tags'))

@ip_management_bp.route('/ip/group/tags/delete/<int:tag_id>', methods=['GET'])
@restriction.login_required
@restriction.admin_required
def delete_ip_group_tag(tag_id):
    try:
        response = requests.delete(
            f'http://localhost:8080/api/private/ip/groups/tag/{tag_id}',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id'),
                'ip_group_tag_id': tag_id
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('Tag deleted successfully', 'success')
                return redirect(url_for('ip_management.ip_group_tags'))
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete tag')
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('ip_management.ip_group_tags'))

@ip_management_bp.route('/ip/group/tags/delete/all', methods=['POST'])
@restriction.login_required
@restriction.admin_required
def delete_all_ip_group_tags():
    try:
        response = requests.delete(
            'http://localhost:8080/api/private/ip/groups/tags/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('All tags deleted successfully', 'success')
                return jsonify({'message': 'All tags deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': 'Failed to delete all tags', 'error': str(e)}), 500
