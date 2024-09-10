from models.users.functions import users_functions as functions
from . import regions_bp
from flask import render_template, redirect, url_for, flash, request, jsonify, session
from app.decorators import RequirementsDecorators as restriction
from entities.region import RegionEntity
from models.regions.models import Region
from utils.threading_manager import ThreadingManager

@regions_bp.route('/', methods=['GET'])
@restriction.login_required  
def regions():
    try:
        region_list = ThreadingManager().run_thread(Region.get_regions, 'r')
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
            region = RegionEntity(  
                region_id=int(),  
                region_name=request.form['region_name']  
            )
            ThreadingManager().run_thread(Region.add_region, 'w', region)
            flash('Region added successfully', 'success')  
            functions.create_log(session['user_id'], 'Region Added', 'INSERT', 'regions')  
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
            region = RegionEntity(  
                region_id=region_id,  
                region_name=request.form['region_name']  
            )
            ThreadingManager().run_thread(Region.update_region, 'w', region)
            flash('Region was updated successfully', 'success')  
            functions.create_log(session['user_id'], 'Region Updated', 'UPDATE', 'regions')  
        except Exception as e:  
            flash(str(e), 'danger')  
        return redirect(url_for('regions.regions'))  
    try:  
        region = ThreadingManager().run_thread(Region.get_region, 'rx', region_id)
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
        ThreadingManager().run_thread(Region.delete_region, 'w', region_id)
        flash('Region deleted successfully', 'success')  
        functions.create_log(session['user_id'], 'Region Deleted', 'DELETE', 'regions')  
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
            ThreadingManager().run_thread(Region.delete_region, 'w', region_id)
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
        ThreadingManager().run_thread(Region.delete_all_regions, 'wx')
        flash('All Regions Deleted Successfully', 'success')  
        functions.create_log(session['user_id'], 'All Regions Deleted', 'DELETE', 'regions')  
        return jsonify({'message': 'Regions deleted successfully'}), 200  
    except Exception as e:  
        flash(str(e), 'danger')  
        return jsonify({'message': 'Failed to delete regions', 'error': str(e)}), 500
