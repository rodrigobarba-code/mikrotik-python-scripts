import requests
from . import sites_bp
from entities.site import SiteEntity
from entities.region import RegionEntity
from app.functions import get_verified_jwt_header
from app.decorators import RequirementsDecorators as restriction
from flask import render_template, redirect, url_for, flash, request, jsonify, session

def get_available_regions() -> list[RegionEntity]:
    region_list = []
    response = requests.get(
        'http://localhost:8080/api/private/regions/',
        headers=get_verified_jwt_header(),
        params={'user_id': session.get('user_id')}
    )
    if response.status_code == 200:
        if response.json().get('backend_status') == 200:
            region_list = [
                RegionEntity(
                    region.get('region_id'),
                    region.get('region_name')
                )
                for region in response.json().get('regions')
            ]
        else:
            raise Exception(response.json().get('message'))
    elif response.status_code == 500:
        raise Exception('Failed to retrieve regions')
    return region_list

@sites_bp.route('/', methods=['GET'])
@restriction.login_required  
def sites():
    try:
        response = requests.get(
            'http://localhost:8080/api/private/sites/', 
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                site_list = [
                    SiteEntity(
                        site_id=site.get('site_id'),
                        site_name=site.get('site_name'),
                        fk_region_id=site.get('fk_region_id'),
                        region_name=site.get('region_name'),
                        site_segment=site.get('site_segment')
                    )
                    for site in response.json().get('sites')
                ]
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve sites')
        return render_template(
            'sites/sites.html',
            site_list=site_list,  
            site=None
        )
    except Exception as e:  
        flash(str(e), 'danger')  
        return redirect(url_for('sites.sites'))

@sites_bp.route('/add', methods=['GET', 'POST'])
@restriction.login_required  
@restriction.admin_required  
def add_site():
    if request.method == 'POST':  
        try:
            response = requests.post(
                'http://localhost:8080/api/private/site/',
                headers=get_verified_jwt_header(),
                params={
                    'user_id': session.get('user_id'),
                    'fk_region_id': int(request.form['fk_region_id']),
                    'site_name': request.form['site_name'],
                    'site_segment': int(request.form['site_segment'])
                }
            )
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    flash('Site added successfully', 'success')
                else:
                    raise Exception(response.json().get('message'))
            elif response.status_code == 500:
                raise Exception('Failed to add site')
        except Exception as e:
            flash(str(e), 'danger')
        return redirect(url_for('sites.sites'))

    try:
        region_list = get_available_regions()
        return render_template(
            'sites/form_sites.html',
            region_list=region_list,
            site=None
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('sites.sites'))

@sites_bp.route('/update/<int:site_id>', methods=['GET', 'POST'])
@restriction.login_required  
@restriction.admin_required  
def update_site(site_id):
    try:
        response = requests.get(
            f'http://localhost:8080/api/private/site/{site_id}',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                site_obj = response.json().get('site')
                site = SiteEntity(
                    site_obj.get('site_id'),
                    site_obj.get('site_name'),
                    site_obj.get('fk_region_id'),
                    site_obj.get('region_name'),
                    site_obj.get('site_segment')
                )
            else:
                flash(response.json().get('message'), 'danger')
                return redirect(url_for('sites.sites'))
        elif response.status_code == 500:
            flash('Failed to retrieve site', 'danger')
            return redirect(url_for('sites.sites'))
    except Exception as e:
        flash(str(e), 'danger')

    if request.method == 'POST':
        try:
            response = requests.put(
                f'http://localhost:8080/api/private/site/{site_id}',
                headers=get_verified_jwt_header(),
                params={
                    'user_id': session.get('user_id'),
                    'site_id': site_id,
                    'fk_region_id': int(request.form['fk_region_id']),
                    'site_name': request.form['site_name'],
                    'site_segment': int(request.form['site_segment'])
                }
            )
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    flash('Site updated successfully', 'success')
                else:
                    raise Exception(response.json().get('message'))
            elif response.status_code == 500:
                raise Exception('Failed to update site')
        except Exception as e:
            flash(str(e), 'danger')
        return redirect(url_for('sites.sites'))

    try:
        region_list = get_available_regions()
        return render_template(
            'sites/form_sites.html',
            region_list=region_list,
            site=site
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('sites.sites'))

@sites_bp.route('/delete/<int:site_id>', methods=['GET'])
@restriction.login_required  
@restriction.admin_required  
def delete_site(site_id):
    try:
        response = requests.delete(
            f'http://localhost:8080/api/private/site/{site_id}',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('Site deleted successfully', 'success')
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete site')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('sites.sites'))

@sites_bp.route('/delete/bulk', methods=['POST'])
@restriction.login_required  
@restriction.admin_required  
def bulk_delete_site():
    data = request.get_json()
    sites_ids = data.get('items_ids', [])
    try:
        response = requests.delete(
            'http://localhost:8080/api/private/sites/bulk/',
            json={'sites_ids': sites_ids},
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flag = response.json().get('count_flag')
                flash('Sites deleted successfully', 'success')

                return jsonify({'message': f'{flag} sites deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            return jsonify({'message': 'Failed to delete sites'}), 500
    except Exception as e:
        flash(str(e), 'danger')
    return jsonify({'message': 'Failed to delete sites', 'error': str(e)}), 500

@sites_bp.route('/delete/all', methods=['POST'])
@restriction.login_required  
@restriction.admin_required  
def delete_all_sites():
    try:  
        response = requests.delete(
            'http://localhost:8080/api/private/sites/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('All Sites Deleted Successfully', 'success')

                return jsonify({'message': 'All sites deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            return jsonify({'message': 'Failed to delete sites'}), 500
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': 'Failed to delete sites', 'error': str(e)}), 500

@sites_bp.route('/import/excel', methods=['POST'])
@restriction.login_required
@restriction.admin_required
def import_sites_from_excel():
    try:
        import pandas as pd

        file = request.files['file']

        if file.filename.split('.')[-1] not in ['xls', 'xlsx']:
            raise Exception('Invalid file format')

        df = pd.read_excel(file)
        df = df.where(pd.notnull(df), None)

        json_site_list = []
        for index, row in df.iterrows():
            site = {
                'site_name': row['Site Name'],
                'fk_region_id': int(row['Region ID']),
                'site_segment': int(row['Segment'])
            }
            json_site_list.append(site)

        response = requests.post(
            'http://localhost:8080/api/private/bulk/insert/sites/',
            json={'sites': json_site_list},
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash(response.json().get('message'), 'success')
                return jsonify(
                    {'message': response.json().get('message')}
                ), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to import sites from excel')
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': str(e)}), 500
    return redirect(url_for('sites.sites'))
