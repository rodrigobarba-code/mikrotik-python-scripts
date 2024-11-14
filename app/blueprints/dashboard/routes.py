import requests
from . import dashboard_bp
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.decorators import RequirementsDecorators as restriction
from app.functions import get_verified_jwt_header
from flask import render_template, flash, session


# Function to Fetch URL
def fetch_url(url, user_id):
    try:
        response = requests.get(
            url,
            headers=get_verified_jwt_header(),
            params={'user_id': user_id}  # Pass user_id explicitly
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                return response.json().get('data')
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to fetch data from the server')
    except Exception as e:
        flash(str(e), 'danger')
        return None  # Return None in case of an error


# URLS Dictionary
urls = {
    'total_ips': 'http://localhost:8080/api/private/dashboard/get/total/ips/on/database/',
    'duplicated_ips': 'http://localhost:8080/api/private/dashboard/get/duplicated/ip/with/indexes/',
    'total_segments_per_site': 'http://localhost:8080/api/private/dashboard/get/total/segments/per/site/',
    'available_public_ip_per_site': 'http://localhost:8080/api/private/dashboard/get/available/public/ip/per/site/',
    'available_private_ip_per_site': 'http://localhost:8080/api/private/dashboard/get/available/private/ip/per/site/',
    'assigned_public_ip_per_site': 'http://localhost:8080/api/private/dashboard/get/assigned/public/ip/per/site/',
    'assigned_private_ip_per_site': 'http://localhost:8080/api/private/dashboard/get/assigned/private/ip/per/site/'
}


# Function to Get Site Names
def get_site_names():
    try:
        response = requests.get(
            'http://localhost:8080/api/private/sites/',
            headers=get_verified_jwt_header(),
            params={'user_id': session.get('user_id')}  # Pass user_id explicitly
        )
        if response.status_code == 200:
            if response.json().get('backend_status') == 200:
                site_list = [
                    (site.get('site_id'), site.get('site_name')) for site in response.json().get('sites')
                ]
                return site_list
            else:
                raise Exception(response.json().get('message'))
        elif response.status_code == 500:
            raise Exception('Failed to fetch data from the server')
    except Exception as e:
        flash(str(e), 'danger')
        return None  # Return None in case of an error


# Dashboard Main Route
@dashboard_bp.route('/', methods=['GET'])
@restriction.login_required  # Login Required Decorator
@restriction.admin_required  # Admin Required Decorator
def dashboard():
    # Get user_id from session
    user_id = session.get('user_id')

    # Using ThreadPoolExecutor to fetch multiple URLs concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Execute all fetch URL calls concurrently
        future_to_key = {executor.submit(fetch_url, url, user_id): key for key, url in urls.items()}
        results = {}

        # Wait for all futures to complete
        for future in as_completed(future_to_key):
            key = future_to_key[future]
            data = future.result()
            results[key] = data

    return render_template(
        'dashboard/dashboard.html',
        dashboard_data=results,
        sites=get_site_names()
    )  # Rendering Dashboard Template
