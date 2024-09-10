from models.users.functions import users_functions as functions
from . import regions_bp
from flask import render_template, redirect, url_for, flash, request, jsonify, session
from app.decorators import RequirementsDecorators as restriction
import requests
from entities.region import RegionEntity

@regions_bp.route('/', methods=['GET'])
@restriction.login_required  
def regions():
    try:
        region_list = []
        response = requests.get('http://localhost:8080/api/regions/')
        if response.status_code == 200:
            for region in response.json():
                region_list.append(RegionEntity(**region))
        else:
            region_list = []
        return render_template(
            'regions/regions.html',  
            region_list=region_list, region=None  
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
            response = requests.post('http://localhost:8080/api/regions/',
                                     params={'region_name': request.form['region_name']})
            if response.status_code == 200:
                flash('Region added successfully', 'success')
                functions.create_log(session['user_id'], 'Region Added', 'INSERT', 'regions')
            else:
                flash('Failed to add region', 'danger')
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
            response = requests.put(f'http://localhost:8080/api/regions/{region_id}',
                                    params={'region_id': region_id, 'region_name': request.form['region_name']})
            if response.status_code == 200:
                flash('Region updated successfully', 'success')
                functions.create_log(session['user_id'], 'Region Updated', 'UPDATE', 'regions')
            else:
                flash('Failed to update region', 'danger')
        except Exception as e:  
            flash(str(e), 'danger')  
        return redirect(url_for('regions.regions'))  
    try:
        response = requests.get(f'http://localhost:8080/api/regions/{region_id}')
        if response.status_code == 200:
            region = RegionEntity(response.json().get('region_id'), response.json().get('region_name'))
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
        response = requests.delete(f'http://localhost:8080/api/regions/{region_id}')

        if response.status_code == 200:
            flash('Region deleted successfully', 'success')
            functions.create_log(session['user_id'], 'Region Deleted', 'DELETE', 'regions')
        else:
            flash('Failed to delete region', 'danger')
    except Exception as e:  
        flash(str(e), 'danger')  
    return redirect(url_for('regions.regions'))  

@regions_bp.route('/delete/bulk', methods=['POST'])
@restriction.login_required  
@restriction.admin_required  
def bulk_delete_region():
    data = request.get_json()  
    regions_ids = data.get('items_ids', [])  
    try:
        flag = 0  
        for region_id in regions_ids:  
            requests.delete(f'http://localhost:8080/api/regions/{region_id}')
            flag += 1  
        flash(f'{flag} Regions Deleted Successfully', 'success')  
        functions.create_log(session['user_id'], f'{flag} Regions Deleted', 'DELETE', 'regions')  
        return jsonify({'message': 'Regions deleted successfully'}), 200  
    except Exception as e:  
        flash(str(e), 'danger')  
        return jsonify({'message': 'Failed to delete regions', 'error': str(e)}), 500  

@regions_bp.route('/delete/all', methods=['POST'])
@restriction.login_required  
@restriction.admin_required  
def delete_all_regions():
    try:  
        response = requests.delete('http://localhost:8080/api/regions/')
        if response.status_code == 200:
            flash('All Regions Deleted Successfully', 'success')
            functions.create_log(session['user_id'], 'All Regions Deleted', 'DELETE', 'regions')
            return jsonify({'message': 'Regions deleted successfully'}), 200
        else:
            flash('Failed to delete regions', 'danger')
            return jsonify({'message': 'Failed to delete regions'}), 500
    except Exception as e:  
        flash(str(e), 'danger')  
        return jsonify({'message': 'Failed to delete regions', 'error': str(e)}), 500
