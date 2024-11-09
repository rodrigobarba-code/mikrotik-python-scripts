from ...auth import verify_jwt
from fastapi import APIRouter, Depends, Request
from utils.threading_manager import ThreadingManager

from ...functions import APIFunctions
from models.dashboard.functions import DashboardFunctions
# from models.router_scan.models import ARPTag

dashboard_router = APIRouter()
dashboard_functions = APIFunctions()

@dashboard_router.get("/dashboard/get/assigned/private/ip/per/site")
async def get_assigned_private_ip_per_site(
    user_id: int,
    metadata: Request
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

@dashboard_router.get("/dashboard/get/assigned/public/ip/per/site")
async def get_assigned_public_ip_per_site(
    user_id: int,
    metadata: Request
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