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


@dashboard_bp.route('/', methods=['GET'])
@restriction.login_required  # Login Required Decorator
def dashboard():
    # Obtener el user_id desde la sesión
    user_id = session.get('user_id')

    # Usar ThreadPoolExecutor para llamar a los endpoints simultáneamente
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Llamar a los endpoints necesarios
        assigned_future = executor.submit(fetch_url, urls['assigned_private_ip_per_site'], user_id)
        available_future = executor.submit(fetch_url, urls['available_private_ip_per_site'], user_id)
        available_public_future = executor.submit(fetch_url, urls['available_public_ip_per_site'], user_id)
        assigned_public_future = executor.submit(fetch_url, urls['assigned_public_ip_per_site'], user_id)
        total_ips_future = executor.submit(fetch_url, urls['total_ips'], user_id)

        # Obtener resultados
        assigned_data = assigned_future.result()
        available_data = available_future.result()
        available_public_data = available_public_future.result()
        assigned_public_data = assigned_public_future.result()
        total_ips_data = total_ips_future.result()

    # Procesar los datos combinados por sitio
    combined_data = {}
    for site, site_data in assigned_data.items():
        combined_data[site] = {
            "assigned": site_data["by_segment"],
            "available": available_data.get(site, {}).get("by_segment", [])
        }

    # Procesar los datos de IPs públicas
    public_ips_data = {}
    for site, site_data in assigned_public_data.items():
        public_ips_data[site] = {
            "assigned": site_data["by_segment"],
            "available": available_public_data.get(site, {}).get("by_segment", [])
        }

    # Renderizar el template con los datos preparados
    return render_template(
        'dashboard/dashboard.html',
        dashboard_data=combined_data,  # Datos combinados de IPs asignadas y disponibles
        public_ips_data=public_ips_data,  # Datos de IPs púb
        total_ips_data=total_ips_data,  # Datos de total_ips
        sites=get_site_names()  # Lista de sitios para los filtros
    )
