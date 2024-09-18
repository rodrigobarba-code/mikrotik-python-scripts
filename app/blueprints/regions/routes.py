import requests
from . import regions_bp
from entities.region import RegionEntity
from app.functions import get_verified_jwt_header
from models.users.functions import users_functions as functions
from app.decorators import RequirementsDecorators as restriction
from flask import render_template, redirect, url_for, flash, request, jsonify, session

@regions_bp.route('/', methods=['GET'])
@restriction.login_required  
def regions():
    try:
        response = requests.get('http://localhost:8080/api/private/regions/', headers=get_verified_jwt_header())
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                region_list = [
                    RegionEntity(region.get('region_id'), region.get('region_name'))
                    for region in response.json().get('regions')
                ]
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve regions')
        return render_template(
            'regions/regions.html',  
            region_list=region_list,
            region=None
        )
    except Exception as e:  
        flash(str(e), 'danger')  
        return redirect(url_for('regions.regions'))  

@regions_bp.route('/add', methods=['GET', 'POST'])
@restriction.login_required  
@restriction.admin_required  
def add_region():
    if request.method == 'POST':  
        try:
            response = requests.post('http://localhost:8080/api/private/region/',
                                     params={'region_name': request.form['region_name']}, headers=get_verified_jwt_header())
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    flash('Region added successfully', 'success')
                    functions.create_log(session['user_id'], 'Region Added', 'CREATE', 'regions')
                else:
                    raise Exception(response.json().get('message'))
            elif response.status_code == 500:
                raise Exception('Failed to add region')
        except Exception as e:
            flash(str(e), 'danger')
        return redirect(url_for('regions.regions'))
    return render_template(
        'regions/form_regions.html',
        region=None
    )

@regions_bp.route('/update/<int:region_id>', methods=['GET', 'POST'])
@restriction.login_required  
@restriction.admin_required  
def update_region(region_id):
    if request.method == 'POST':
        try:  
            response = requests.put(f'http://localhost:8080/api/private/region/{region_id}',
                                    params={'region_id': region_id, 'region_name': request.form['region_name']}, headers=get_verified_jwt_header())
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    flash('Region updated successfully', 'success')
                    functions.create_log(session['user_id'], 'Region Updated', 'UPDATE', 'regions')
                else:
                    raise Exception(response.json().get('message'))
            else:
                raise Exception('Failed to update region')
        except Exception as e:  
            flash(str(e), 'danger')  
        return redirect(url_for('regions.regions'))  
    try:
        response = requests.get(f'http://localhost:8080/api/private/region/{region_id}', headers=get_verified_jwt_header())
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                region_object = response.json().get('region')
                region = RegionEntity(
                    region_object.get('region_id'),
                    region_object.get('region_name')
                )
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve region')
        return render_template(
            'regions/form_regions.html',  
            region=region
        )
    except Exception as e:  
        flash(str(e), 'danger')  
        return redirect(url_for('regions.regions'))  

@regions_bp.route('/delete/<int:region_id>', methods=['GET'])
@restriction.login_required  
@restriction.admin_required  
def delete_region(region_id):
    try:  
        response = requests.delete(f'http://localhost:8080/api/private/region/{region_id}', headers=get_verified_jwt_header())
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('Region Deleted Successfully', 'success')
                functions.create_log(session['user_id'], 'Region Deleted', 'DELETE', 'regions')
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete region')
    except Exception as e:  
        flash(str(e), 'danger')  
    return redirect(url_for('regions.regions'))  

@regions_bp.route('/delete/bulk', methods=['POST'])
@restriction.login_required  
@restriction.admin_required  
def bulk_delete_region():
    data = request.get_json()  
    regions_ids = data.get('items_ids', [])
    regions_ids = [int(region_id) for region_id in regions_ids]
    try:
        response = requests.delete('http://localhost:8080/api/private/regions/bulk/',
                                   json={'regions_ids': regions_ids}, headers=get_verified_jwt_header())
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flag = response.json().get('count_flag')
                flash(f'{flag} Regions Deleted Successfully', 'success')
                functions.create_log(session['user_id'], 'Bulk Regions Deleted', 'DELETE', 'regions')

                return jsonify({'message': f'{flag} regions deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            return jsonify({'message': 'Failed to delete regions'}), 500
    except Exception as e:  
        flash(str(e), 'danger')  
        return jsonify({'message': 'Failed to delete regions', 'error': str(e)}), 500

@regions_bp.route('/delete/all', methods=['POST'])
@restriction.login_required  
@restriction.admin_required  
def delete_all_regions():
    try:  
        response = requests.delete('http://localhost:8080/api/private/regions/', headers=get_verified_jwt_header())
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('All Regions Deleted Successfully', 'success')
                functions.create_log(session['user_id'], 'All Regions Deleted', 'DELETE', 'regions')

                return jsonify({'message': 'All regions deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            return jsonify({'message': 'Failed to delete regions'}), 500
    except Exception as e:  
        flash(str(e), 'danger')  
        return jsonify({'message': 'Failed to delete regions', 'error': str(e)}), 500
