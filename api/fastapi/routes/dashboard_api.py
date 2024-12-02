from ...auth import verify_jwt
from fastapi import APIRouter, Depends, Request

from ...functions import APIFunctions
from models.dashboard.functions import DashboardFunctions
dashboard_router = APIRouter()
dashboard_functions = APIFunctions()

@dashboard_router.get("/dashboard/get/assigned/private/ip/per/site/")
async def get_assigned_private_ip_per_site(
    user_id: int,
    metadata: Request,
    token: str = Depends(verify_jwt)
):
    try:
        # Verify the user existence
        if dashboard_functions.verify_user_existence(user_id):
            # Get the result
            request = DashboardFunctions.get_assigned_ip_per_site(type="private")

            # Create a transaction log
            dashboard_functions.create_transaction_log(
                action="GET",
                table="ip_management",
                user_id=int(user_id),
                description="Retrieved the assigned private IP per site",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )

            # Return the result
            return {
                'message': "Successfully retrieved the assigned private IP per site",
                'data': request,
                'backend_status': 200
            }
        else:
            # Raise an exception
            raise Exception("User not registered in the system")
    except Exception as e:
        # Return the error message
        return {
            'message': f"An error occurred: {str(e)}",
            'backend_status': 400
        }

@dashboard_router.get("/dashboard/get/assigned/public/ip/per/site/")
async def get_assigned_public_ip_per_site(
    user_id: int,
    metadata: Request,
    token: str = Depends(verify_jwt)
):
    try:
        # Verify the user existence
        if dashboard_functions.verify_user_existence(user_id):
            # Get the result
            request = DashboardFunctions.get_assigned_ip_per_site(type="public")

            # Create a transaction log
            dashboard_functions.create_transaction_log(
                action="GET",
                table="ip_management",
                user_id=int(user_id),
                description="Retrieved the assigned public IP per site",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )

            # Return the result
            return {
                'message': "Successfully retrieved the assigned public IP per site",
                'data': request,
                'backend_status': 200
            }
        else:
            # Raise an exception
            raise Exception("User not registered in the system")
    except Exception as e:
        # Return the error message
        return {
            'message': f"An error occurred: {str(e)}",
            'backend_status': 400
        }

@dashboard_router.get("/dashboard/get/available/private/ip/per/site/")
async def get_available_private_ip_per_site(
    user_id: int,
    metadata: Request,
    token: str = Depends(verify_jwt)
):
    try:
        # Verify the user existence
        if dashboard_functions.verify_user_existence(user_id):
            # Get the result
            request = DashboardFunctions.get_available_ip_per_site(type="private")

            # Create a transaction log
            dashboard_functions.create_transaction_log(
                action="GET",
                table="ip_management",
                user_id=int(user_id),
                description="Retrieved the available private IP per site",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )

            # Return the result
            return {
                'message': "Successfully retrieved the available private IP per site",
                'data': request,
                'backend_status': 200
            }
        else:
            # Raise an exception
            raise Exception("User not registered in the system")
    except Exception as e:
        # Return the error message
        return {
            'message': f"An error occurred: {str(e)}",
            'backend_status': 400
        }

@dashboard_router.get("/dashboard/get/available/public/ip/per/site/")
async def get_available_public_ip_per_site(
    user_id: int,
    metadata: Request,
    token: str = Depends(verify_jwt)
):
    try:
        # Verify the user existence
        if dashboard_functions.verify_user_existence(user_id):
            # Get the result
            request = DashboardFunctions.get_available_ip_per_site(type="public")

            # Create a transaction log
            dashboard_functions.create_transaction_log(
                action="GET",
                table="ip_management",
                user_id=int(user_id),
                description="Retrieved the available public IP per site",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )

            # Return the result
            return {
                'message': "Successfully retrieved the available public IP per site",
                'data': request,
                'backend_status': 200
            }
        else:
            # Raise an exception
            raise Exception("User not registered in the system")
    except Exception as e:
        # Return the error message
        return {
            'message': f"An error occurred: {str(e)}",
            'backend_status': 400
        }

@dashboard_router.get("/dashboard/get/duplicated/ip/with/indexes/")
async def get_duplicated_ip_with_indexes(
    user_id: int,
    metadata: Request,
    token: str = Depends(verify_jwt)
):
    try:
        # Verify the user existence
        if dashboard_functions.verify_user_existence(user_id):
            # Get the result
            request = DashboardFunctions.get_duplicated_ip_with_indexes()

            # Create a transaction log
            dashboard_functions.create_transaction_log(
                action="GET",
                table="ip_management",
                user_id=int(user_id),
                description="Retrieved the duplicated IP with indexes",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )

            # Return the result
            return {
                'message': "Successfully retrieved the duplicated IP with indexes",
                'data': request,
                'backend_status': 200
            }
        else:
            # Raise an exception
            raise Exception("User not registered in the system")
    except Exception as e:
        # Return the error message
        return {
            'message': f"An error occurred: {str(e)}",
            'backend_status': 400
        }

@dashboard_router.get("/dashboard/get/total/ips/on/database/")
async def get_total_ips_on_database(
    user_id: int,
    metadata: Request,
    token: str = Depends(verify_jwt)
):
    try:
        # Verify the user existence
        if dashboard_functions.verify_user_existence(user_id):
            # Get the result
            request = DashboardFunctions.get_total_ips_on_database()

            # Create a transaction log
            dashboard_functions.create_transaction_log(
                action="GET",
                table="ip_management",
                user_id=int(user_id),
                description="Retrieved the total IPs on the database",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )

            # Return the result
            return {
                'message': "Successfully retrieved the total IPs on the database",
                'data': request,
                'backend_status': 200
            }
        else:
            # Raise an exception
            raise Exception("User not registered in the system")
    except Exception as e:
        # Return the error message
        return {
            'message': f"An error occurred: {str(e)}",
            'backend_status': 400
        }

@dashboard_router.get("/dashboard/get/total/segments/per/site/")
async def get_total_segments_per_site(
    user_id: int,
    metadata: Request
):
    try:
        # Verify the user existence
        if dashboard_functions.verify_user_existence(user_id):
            # Get the result
            request = DashboardFunctions.get_total_segments_per_site()

            # Create a transaction log
            dashboard_functions.create_transaction_log(
                action="GET",
                table="ip_management",
                user_id=int(user_id),
                description="Retrieved the total segments per site",
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )

            # Return the result
            return {
                'message': "Successfully retrieved the total segments per site",
                'data': request,
                'backend_status': 200
            }
        else:
            # Raise an exception
            raise Exception("User not registered in the system")
    except Exception as e:
        # Return the error message
        return {
            'message': f"An error occurred: {str(e)}",
            'backend_status': 400
        }
