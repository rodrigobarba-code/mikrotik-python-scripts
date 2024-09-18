import requests
from . import sites_bp
from entities.site import SiteEntity
from entities.region import RegionEntity
from app.functions import get_verified_jwt_header
from models.users.functions import users_functions as functions
from app.decorators import RequirementsDecorators as restriction
from flask import render_template, redirect, url_for, flash, request, jsonify, session

def get_available_regions() -> list[RegionEntity]:
    region_list = []
    response = requests.get('http://localhost:8080/api/private/regions/', headers=get_verified_jwt_header())
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
        response = requests.get('http://localhost:8080/api/private/sites/', headers=get_verified_jwt_header())
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
            response = requests.post('http://localhost:8080/api/private/site/',
                                     params={
                                         'fk_region_id': int(request.form['fk_region_id']),
                                         'site_name': request.form['site_name'],
                                         'site_segment': int(request.form['site_segment'])
                                     }, headers=get_verified_jwt_header())
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    flash('Site added successfully', 'success')
                    functions.create_log(session['user_id'], 'Site Added', 'CREATE', 'sites')
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
        response = requests.get(f'http://localhost:8080/api/private/site/{site_id}', headers=get_verified_jwt_header())
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
            response = requests.put(f'http://localhost:8080/api/private/site/{site_id}',
                                    params={
                                        'site_id': site_id,
                                        'fk_region_id': int(request.form['fk_region_id']),
                                        'site_name': request.form['site_name'],
                                        'site_segment': int(request.form['site_segment'])
                                    }, headers=get_verified_jwt_header())
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    flash('Site updated successfully', 'success')
                    functions.create_log(session['user_id'], 'Site Updated', 'UPDATE', 'sites')
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
        response = requests.delete(f'http://localhost:8080/api/private/site/{site_id}', headers=get_verified_jwt_header())
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('Site deleted successfully', 'success')
                functions.create_log(session['user_id'], 'Site Deleted', 'DELETE', 'sites')
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
        response = requests.delete('http://localhost:8080/api/private/sites/bulk/',
                                   json={'sites_ids': sites_ids}, headers=get_verified_jwt_header())
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flag = response.json().get('count_flag')
                flash('Sites deleted successfully', 'success')
                functions.create_log(session['user_id'], 'Sites Deleted', 'DELETE', 'sites')

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
        response = requests.delete('http://localhost:8080/api/private/sites/', headers=get_verified_jwt_header())
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('All Sites Deleted Successfully', 'success')
                functions.create_log(session['user_id'], 'Sites Deleted', 'DELETE', 'sites')

                return jsonify({'message': 'All sites deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            return jsonify({'message': 'Failed to delete sites'}), 500
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': 'Failed to delete sites', 'error': str(e)}), 500
