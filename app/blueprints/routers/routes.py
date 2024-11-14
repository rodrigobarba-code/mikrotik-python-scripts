import requests
from . import routers_bp
from entities.site import SiteEntity
from entities.router import RouterEntity
from app.functions import get_verified_jwt_header
from app.decorators import RequirementsDecorators as restriction
from flask import render_template, redirect, url_for, flash, request, jsonify, session

switch_scan_status = {'enable': True}

async def get_site_name(site_id: int) -> str:
    response = requests.get(
        f'http://localhost:8080/api/private/site/{site_id}',
        headers=get_verified_jwt_header(),
        params={'user_id': session.get('user_id')}
    )
    if response.status_code == 200:
        if response.json().get('backend_status') == 200:
            return response.json().get('site').get('site_name')
        else:
            raise Exception(response.json().get('message'))
    elif response.status_code == 500:
        raise Exception('Failed to retrieve site name')

def get_available_sites() -> list[SiteEntity]:
    site_list = []
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
                    fk_region_id=site.get('fk_region_id'),
                    region_name=str(),
                    site_name=site.get('site_name'),
                    site_segment=site.get('site_segment')
                )
                for site in response.json().get('sites')
            ]
        else:
            raise Exception(response.json().get('message'))
    elif response.status_code == 500:
        raise Exception('Failed to retrieve sites')
    return site_list

@routers_bp.route('/', methods=['GET'])
@restriction.login_required  
def routers():
    try:
        response = requests.get(
            'http://localhost:8080/api/private/routers/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                router_list = [
                    RouterEntity(
                        router_id=router.get('router_id'),
                        router_name=router.get('router_name'),
                        router_description=router.get('router_description'),
                        router_brand=router.get('router_brand'),
                        router_model=router.get('router_model'),
                        router_serial=router.get('router_serial'),
                        fk_site_id=router.get('fk_site_id'),
                        router_ip=router.get('router_ip'),
                        router_mac=router.get('router_mac'),
                        router_username=router.get('router_username'),
                        router_password=router.get('router_password'),
                        allow_scan=router.get('allow_scan')
                    )
                    for router in response.json().get('routers')
                ]
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to retrieve routers')
        return render_template(
            'routers/routers.html',
            switch_scan_status=switch_scan_status['enable'],
            router_list=router_list,
            router=None,
        )
    except Exception as e:  
        flash(str(e), 'danger')  
        return redirect(url_for('routers.routers'))  

@routers_bp.route('/add', methods=['GET', 'POST'])
@restriction.login_required  
@restriction.admin_required   
def add_router():
    if request.method == 'POST':  
        try:  
            response = requests.post(
                'http://localhost:8080/api/private/router/',
                headers=get_verified_jwt_header(),
                params={
                    'user_id': session.get('user_id'),
                    'router_name': request.form['router_name'],
                    'router_description': request.form['router_description'],
                    'router_brand': 'Mikrotik',
                    'router_model': request.form['router_model'],
                    'router_serial': request.form['router_serial'],
                    'fk_site_id': int(request.form['fk_site_id']),
                    'router_ip': request.form['router_ip'],
                    'router_mac': request.form['router_mac'],
                    'router_username': request.form['router_username'],
                    'router_password': request.form['router_password'],
                    'allow_scan': 1 if request.form.get('allow_scan') else 0
                }
            )
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    flash('Router added successfully', 'success')
                    return redirect(url_for('routers.routers'))
                else:
                    raise Exception(response.json().get('message'))
            elif response.status_code == 500:
                raise Exception('Failed to add router')
        except Exception as e:  
            flash(str(e), 'danger')  
        return redirect(url_for('routers.routers'))

    try:
        site_list = get_available_sites()
        return render_template(
            'routers/form_routers.html',
            site_list=site_list,
            router=None
        )
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('routers.routers'))

@routers_bp.route('/update/<int:router_id>', methods=['GET', 'POST'])
@restriction.login_required  
@restriction.admin_required  
def update_router(router_id):
    try:
        response = requests.get(
            f'http://localhost:8080/api/private/router/{router_id}',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                router_obj = response.json().get('router')
                router = RouterEntity(
                    router_id=router_obj.get('router_id'),
                    router_name=router_obj.get('router_name'),
                    router_description=router_obj.get('router_description'),
                    router_brand=router_obj.get('router_brand'),
                    router_model=router_obj.get('router_model'),
                    router_serial=router_obj.get('router_serial'),
                    fk_site_id=router_obj.get('fk_site_id'),
                    router_ip=router_obj.get('router_ip'),
                    router_mac=router_obj.get('router_mac'),
                    router_username=router_obj.get('router_username'),
                    router_password=router_obj.get('router_password'),
                    allow_scan=router_obj.get('allow_scan')
                )
            else:
                flash(response.json().get('message'), 'danger')
                return redirect(url_for('routers.routers'))
        elif response.status_code == 500:
            flash('Failed to retrieve router', 'danger')
            return redirect(url_for('routers.routers'))
    except Exception as e:
        flash(str(e), 'danger')

    if request.method == 'POST':  
        try:  
            response = requests.put(
                f'http://localhost:8080/api/private/router/{router_id}',
                headers=get_verified_jwt_header(),
                params={
                    'user_id': session.get('user_id'),
                    ''
                    'router_name': request.form['router_name'],
                    'router_description': request.form['router_description'],
                    'router_brand': 'Mikrotik',
                    'router_model': request.form['router_model'],
                    'router_serial': request.form['router_serial'],
                    'fk_site_id': int(request.form['fk_site_id']),
                    'router_ip': request.form['router_ip'],
                    'router_mac': request.form['router_mac'],
                    'router_username': request.form['router_username'],
                    'router_password': request.form['router_password'],
                    'allow_scan': 1 if request.form.get('allow_scan') else 0
                }
            )
            if response.status_code == 200:
                if response.json().get('backend_status') == 200:
                    flash('Router updated successfully', 'success')
                else:
                    raise Exception(response.json().get('message'))
            elif response.status_code == 500:
                raise Exception('Failed to update router')
        except Exception as e:  
            flash(str(e), 'danger')
        return redirect(url_for('routers.routers'))

    try:
        site_list = get_available_sites()
        return render_template(  
            'routers/form_routers.html',  
            site_list=site_list,  
            router=router  
        )
    except Exception as e:  
        flash(str(e), 'danger')  
        return redirect(url_for('routers.routers'))  

@routers_bp.route('/delete/<int:router_id>', methods=['GET'])
@restriction.login_required  
@restriction.admin_required  
def delete_router(router_id):
    try:  
        response = requests.delete(
            f'http://localhost:8080/api/private/router/{router_id}',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('Router deleted successfully', 'success')
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete router')
    except Exception as e:  
        flash(str(e), 'danger')  
    return redirect(url_for('routers.routers'))

@routers_bp.route('/delete/bulk', methods=['POST'])
@restriction.login_required  
@restriction.admin_required  
def bulk_delete_router():
    data = request.get_json()  
    routers_ids = data.get('items_ids', [])  
    try:
        response = requests.delete(
            'http://localhost:8080/api/private/routers/bulk/',
            json={'routers_ids': routers_ids},
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
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

@routers_bp.route('/delete/all', methods=['POST'])
@restriction.login_required  
@restriction.admin_required  
def delete_all_routers():
    try:  
        response = requests.delete(
            'http://localhost:8080/api/private/routers/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                flash('All Routers deleted successfully', 'success')

                return jsonify({'message': 'All routers deleted successfully'}), 200
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to delete routers')
    except Exception as e:  
        flash(str(e), 'danger')  
        return jsonify({'message': 'Failed to delete routers', 'error': str(e)}), 500

@routers_bp.route('/get_router_details/', methods=['GET'])
async def get_router_details():
    try:
        router_id = request.args.get('id')
        response = requests.get(
            f'http://localhost:8080/api/private/router/{router_id}',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                site_name = await get_site_name(response.json().get('router').get('fk_site_id'))
                router_obj = response.json().get('router')
                return jsonify([{
                    'id': ["Identifier", router_obj.get('router_id')],
                    'name': ["Router Name", router_obj.get('router_name')],
                    'description': ["Router Description", router_obj.get('router_description')],
                    'brand': ["Router Brand", router_obj.get('router_brand')],
                    'model': ["Router Model", router_obj.get('router_model')],
                    'serial': ["Router Serial", router_obj.get('router_serial')],
                    'site': ["Router Site", site_name],
                    'ip': ["Router IP", router_obj.get('router_ip')],
                    'mac': ["Router MAC", router_obj.get('router_mac')],
                    'username': ["Router Username", router_obj.get('router_username')],
                    'allow_scan': ["Allow Scan", True if router_obj.get('allow_scan') else False]
                }]), 200
            else:
                return jsonify({'message': response.json().get('message')}), 500
        elif response.status_code == 500:
            return jsonify({'message': 'Failed to get router details'}), 500
    except Exception as e:
        return jsonify({'message': 'Failed to get router details', 'error': str(e)}), 500

@routers_bp.route('/toggle/switch/scan/status/', methods=['GET'])
@restriction.login_required
@restriction.admin_required
def toggle_switch_scan_status():
    try:
        switch_scan_status['enable'] = not switch_scan_status['enable']
        return jsonify({'status': switch_scan_status['enable']}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to toggle scan status', 'error': str(e)}), 500

@routers_bp.route('/verify/credentials/')
@restriction.login_required
@restriction.admin_required
def verify_router_credentials():
    try:
        router_ip = request.args.get('router_ip')
        router_username = request.args.get('router_username')
        router_password = request.args.get('router_password')

        response = requests.get(
            f'http://localhost:8080/api/private/router/verify-credentials/',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id'),
                'router_ip': router_ip,
                'router_username': router_username,
                'router_password': router_password
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                return jsonify({
                    'message': response.json().get('message'),
                    'is_connected': response.json().get('is_connected')
                }), 200
            else:
                return jsonify({
                    'message': response.json().get('message')
                }), 500
        elif response.status_code == 500:
            return jsonify({
                'message': 'Failed to verify router credentials'
            }), 500
    except Exception as e:
        return jsonify({
            'message': 'Failed to verify router credentials', 'error': str(e)
        }), 500

@routers_bp.route('/verify/<int:router_id>')
@restriction.login_required
@restriction.admin_required
def verify_router(router_id):
    try:
        response = requests.get(
            f'http://localhost:8080/api/private/router/verify/{router_id}',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id')
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                return jsonify({
                    'message': response.json().get('message'),
                    'backend_status': response.json().get('backend_status')
                }), 200
            else:
                return jsonify({
                    'message': response.json().get('message'),
                    'backend_status': response.json().get('backend_status')
                }), 500
        elif response.status_code == 500:
            return jsonify({
                'message': response.json().get('message'),
                'backend_status': response.json().get('backend_status')
            }), 500
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('routers.routers'))

@routers_bp.route('/verify/all')
@restriction.login_required
@restriction.admin_required
def verify_all_routers():
    try:
        response = requests.get(
            'http://localhost:8080/api/private/routers/verify/all/',
            headers=get_verified_jwt_header(),
            params={
                'user_id': session.get('user_id')
            }
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                return jsonify({
                    'message': response.json().get('message'),
                    'backend_status': response.json().get('backend_status'),
                    'is_connected': response.json().get('is_connected')
                }), 200
            else:
                return jsonify({
                    'message': response.json().get('message'),
                    'backend_status': response.json().get('backend_status'),
                    'is_connected': response.json().get('is_connected')
                }), 500
        elif response.status_code == 500:
            return jsonify({
                'message': response.json().get('message'),
                'backend_status': response.json().get('backend_status'),
                'is_connected': response.json().get('is_connected')
            }), 500
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('routers.routers'))

@routers_bp.route('/import/excel', methods=['POST'])
@restriction.login_required
@restriction.admin_required
def import_routers_from_excel():
    try:
        import pandas as pd

        file = request.files['file']

        if file.filename.split('.')[-1] not in ['xls', 'xlsx']:
            raise Exception('Invalid file format')

        df = pd.read_excel(file)
        df = df.where(pd.notnull(df), None)

        json_router_list = []
        for index, row in df.iterrows():
            router = {
                'router_name': row['Router Name'],
                'router_description': row['Router Description'],
                'router_brand': 'Mikrotik',
                'router_model': row['Router Model'],
                'router_serial': row['Router Serial'],
                'fk_site_id': int(row['Site ID']),
                'router_ip': row['Router IP'],
                'router_mac': row['Router MAC'],
                'router_username': row['Router Username'],
                'router_password': row['Router Password'],
                'allow_scan': 1 if row['Allow Scan'] else 0
            }
            json_router_list.append(router)

        response = requests.post(
            'http://localhost:8080/api/private/bulk/insert/routers/',
            json={'routers': json_router_list},
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
            raise Exception('Failed to import routers from excel')
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': str(e)}), 500
    return redirect(url_for('routers.routers'))
