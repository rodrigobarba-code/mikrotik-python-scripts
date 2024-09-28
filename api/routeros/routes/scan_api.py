from ..api import RouterAPI
from ...auth import verify_jwt
from ...functions import APIFunctions
from fastapi import APIRouter, Depends, Request
from concurrent.futures import ThreadPoolExecutor

scan_router = APIRouter()

scan_functions = APIFunctions()

scan_status = ['idle', 'started', 'completed']
scan_flag = {'status': scan_status[0]}

executor = ThreadPoolExecutor(max_workers=2)
global_future = None

@scan_router.get('/scan')
async def scan_routeros(user_id: str, metadata: Request):
    global global_future
    try:
        if scan_functions.verify_user_existence(user_id):
            if scan_flag['status'] == scan_status[0]:
                scan_flag['status'] = scan_status[1]
                global_future = executor.submit(await RouterAPI.arp_scan())
                scan_functions.create_transaction_log(
                    action='GET',
                    table='scan',
                    user_id=int(user_id),
                    description='RouterOS scan initiated',
                    public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
                )
                return {
                    'message': 'RouterOS scan initiated',
                    'backend_status': 200
                }
            else:
                raise Exception('RouterOS scan already in progress')
    except Exception as e:
        return {
            'error': str(e),
            'backend_status': 500
        }

@scan_router.get('/scan/status')
async def scan_status_routeros(user_id: str, metadata: Request, token: str = Depends(verify_jwt)):
    global global_future
    try:
        if scan_functions.verify_user_existence(user_id):
            if global_future is not None:
                if global_future.done():
                    scan_flag['status'] = scan_status[2]
                    global_future = None
                elif global_future.running():
                    scan_flag['status'] = scan_status[1]
            else:
                scan_flag['status'] = scan_status[0]

            scan_functions.create_transaction_log(
                action='GET',
                table='scan',
                user_id=int(user_id),
                description='RouterOS scan status retrieved',
                public=str(str(metadata.client.host) + ':' + str(metadata.client.port))
            )
            return {
                'message': 'RouterOS scan status retrieved, current status: ' + scan_flag['status'],
                'status': scan_flag['status'],
                'backend_status': 200
            }
    except Exception as e:
        return {
            'error': str(e),
            'backend_status': 500
        }
