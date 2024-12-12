import asyncio
from ..api import RouterAPI
from ...auth import verify_jwt
from ...functions import APIFunctions
from fastapi import APIRouter, Depends, Request
import asyncio
from ..api import RouterAPI
from ...auth import verify_jwt
from ...functions import APIFunctions
from fastapi import APIRouter, Depends, Request

scan_router = APIRouter()

scan_functions = APIFunctions()

@scan_router.get('/scan')
async def scan_routeros(user_id: str, metadata: Request):
    try:
        if scan_functions.verify_user_existence(user_id):
            if True:
                asyncio.create_task(RouterAPI.arp_scan())
                scan_functions.create_transaction_log(
                    action='GET',
                    table='scan',
                    user_id=int(user_id),
                    description='RouterOS scan initiated',
                    public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
                )
                return {
                    'message': 'RouterOS scan finished',
                    'backend_status': 200
                }
            else:
                raise Exception('RouterOS scan already in progress')
        else:
            raise Exception('User does not exist in the database')
    except Exception as e:
        return {
            'error': str(e),
            'backend_status': 500
        }

@scan_router.get('/scan/status')
async def scan_status_routeros(user_id: str, metadata: Request, token: str = Depends(verify_jwt)):
    try:
        if scan_functions.verify_user_existence(user_id):
            scan_functions.create_transaction_log(
                action='GET',
                table='scan',
                user_id=int(user_id),
                description='RouterOS scan status requested',
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'scan_status': RouterAPI.get_scan_status(),
                'backend_status': 200
            }
        else:
            raise Exception('User does not exist in the database')
    except Exception as e:
        return {
            'error': str(e),
            'backend_status': 500
        }
