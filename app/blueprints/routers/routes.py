# Importing Required Libraries
from flask import render_template, redirect, url_for, flash, request, jsonify
from . import routers_bp
from app.decorators import RequirementsDecorators as restriction

# Importing Required Libraries

# Importing Required Entities
from app.blueprints.routers.entities import RouterEntity
# Importing Required Entities

# Importing Required Models
from app.blueprints.routers.models import Router
# Importing Required Models

# Routers Main Route
@routers_bp.route('/', methods=['GET'])
@restriction.login_required
def routers():
    router_list = Router.get_all_routers()
    return render_template(
        'routers/routers.html',
        router_list=router_list
    )


# Routers Main Route

# Routers Add Route
@routers_bp.route('/add', methods=['GET', 'POST'])
@restriction.login_required
@restriction.admin_required
def add_router():
    if request.method == 'POST':
        try:
            router = RouterEntity(
                router_id=None,
                router_name=request.form['router_name'],
                router_description=request.form['router_description'],
                router_brand=request.form['router_brand'],
                router_model=request.form['router_model'],
                fk_site_id=int(request.form['fk_site_id']),
                router_ip=request.form['router_ip'],
                router_mac=request.form['router_mac'],
                router_username=request.form['router_username'],
                router_password=request.form['router_password'],
                allow_scan=1 if request.form.get('allow_scan') else 0
            )
            Router.add_router(router)
            flash('Router Added Successfully', 'success')
            return redirect(url_for('routers.routers'))
        except Exception as e:
            flash(str(e), 'danger')
            return render_template('routers/routers.html')
    site_list = Site.get_sites()
    return render_template(
        'routers/form_routers.html',
        site_list=site_list,
        router=None
    )


# Routers Add Route

# Routers Update Route
@routers_bp.route('/update/<int:router_id>', methods=['GET', 'POST'])
@restriction.login_required
@restriction.admin_required
def update_router(router_id):
    if request.method == 'POST':
        try:
            router = RouterEntity(
                router_id=router_id,
                router_name=request.form['router_name'],
                router_description=request.form['router_description'],
                router_brand=request.form['router_brand'],
                router_model=request.form['router_model'],
                fk_site_id=int(request.form['fk_site_id']),
                router_ip=request.form['router_ip'],
                router_mac=request.form['router_mac'],
                router_username=request.form['router_username'],
                router_password=request.form['router_password'],
                allow_scan=1 if request.form.get('allow_scan') else 0
            )
            Router.update_router(router)
            flash('Router Updated Successfully', 'success')
            return redirect(url_for('routers.routers'))
        except Exception as e:
            flash(str(e), 'danger')
            return render_template('routers/routers.html')
    site_list = Site.get_sites()
    router = Router.get_router(router_id)
    return render_template(
        'routers/form_routers.html',
        site_list=site_list,
        router=router
    )


# Routers Update Route

# Routers Delete Route
@routers_bp.route('/delete/<int:router_id>', methods=['GET'])
@restriction.login_required
@restriction.admin_required
def delete_router(router_id):
    try:
        Router.delete_router(router_id)
        flash('Router Deleted Successfully', 'success')
        return redirect(url_for('routers.routers'))
    except Exception as e:
        flash(str(e), 'danger')
        return render_template('routers/routers.html')


# Routers Delete Route

# Routers Bulk Delete Route
@routers_bp.route('/bulk_delete_router', methods=['POST'])
@restriction.login_required
@restriction.admin_required
def bulk_delete_router():
    data = request.get_json()
    router_ids = data.get('router_ids', [])
    print(router_ids)
    try:
        for router_id in router_ids:
            Router.delete_router(router_id)
        flash('Routers Deleted Successfully', 'success')
        return jsonify({'message': 'Routers deleted successfully'}), 200
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': 'Failed to delete routers', 'error': str(e)}), 500


# Routers Bulk Delete Route

# Routers Delete All Route
@routers_bp.route('/delete_all_routers', methods=['POST'])
@restriction.login_required
@restriction.admin_required
def delete_all_routers():
    try:
        Router.delete_all_routers()
        flash('All Routers Deleted Successfully', 'success')
        return jsonify({'message': 'Routers deleted successfully'}), 200
    except Exception as e:
        flash(str(e), 'danger')
        return jsonify({'message': 'Failed to delete routers', 'error': str(e)}), 500


# Routers Delete All Route

# Routers Get Router Details Route
@routers_bp.route('/get_router_details', methods=['POST'])
@restriction.login_required
def get_router_details():
    try:
        data = request.get_json()
        router_id = data.get('router_id', None)
        router = Router.get_router(router_id)
        json_obj = {
            'router_name': router.router_name,
            'router_description': router.router_description,
            'router_brand': router.router_brand,
            'router_model': router.router_model,
            'fk_site_id': Site.get_site(router.fk_site_id).site_name,
            'router_ip': router.router_ip,
            'router_mac': router.router_mac,
            'router_username': router.router_username,
            'router_password': router.router_password,
            'allow_scan': "Yes" if router.allow_scan == 1 else "No"
        }
        return jsonify(json_obj), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get router data', 'error': str(e)}), 500
# Routers Get Router Details Route
